import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
from .models import Equipment, Dataset
from .serializers import DatasetSerializer, EquipmentSerializer

@api_view(['POST'])
def upload_csv(request):
    try:
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.read_csv(file)
        
        # Calculate summary statistics
        summary = {
            "total_count": len(df),
            "avg_flowrate": float(df['Flowrate'].mean()),
            "avg_pressure": float(df['Pressure'].mean()),
            "avg_temperature": float(df['Temperature'].mean()),
            "type_distribution": df['Type'].value_counts().to_dict()
        }
        
        # Create dataset
        dataset = Dataset.objects.create(
            name=file.name,
            total_count=summary['total_count'],
            avg_flowrate=summary['avg_flowrate'],
            avg_pressure=summary['avg_pressure'],
            avg_temperature=summary['avg_temperature'],
            type_distribution=summary['type_distribution']
        )
        
        # Create equipment records
        equipment_list = []
        for _, row in df.iterrows():
            equipment_list.append(Equipment(
                dataset=dataset,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            ))
        Equipment.objects.bulk_create(equipment_list)
        
        # Keep only last 5 datasets
        datasets = Dataset.objects.all()
        if datasets.count() > 5:
            old_datasets = datasets[5:]
            for ds in old_datasets:
                ds.delete()
        
        # Return summary with dataset id
        summary['dataset_id'] = dataset.id
        summary['equipment'] = list(df.to_dict('records'))
        
        return Response(summary, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_datasets(request):
    datasets = Dataset.objects.all()[:5]
    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_dataset_detail(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def generate_pdf_report(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        equipment_list = dataset.equipment.all()
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"<b>Equipment Report - {dataset.name}</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Summary
        summary_text = f"""
        <b>Summary Statistics</b><br/>
        Total Equipment: {dataset.total_count}<br/>
        Average Flowrate: {dataset.avg_flowrate:.2f}<br/>
        Average Pressure: {dataset.avg_pressure:.2f}<br/>
        Average Temperature: {dataset.avg_temperature:.2f}<br/>
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Type Distribution
        type_dist_text = "<b>Type Distribution:</b><br/>"
        for eq_type, count in dataset.type_distribution.items():
            type_dist_text += f"{eq_type}: {count}<br/>"
        elements.append(Paragraph(type_dist_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Equipment Table
        table_data = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for eq in equipment_list:
            table_data.append([
                eq.equipment_name,
                eq.equipment_type,
                str(eq.flowrate),
                str(eq.pressure),
                str(eq.temperature)
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset_id}.pdf"'
        return response
        
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

# ADD THIS FUNCTION at the bottom of backend/equipment/views.py

@api_view(['GET'])
def search_equipment(request):
    """
    Search equipment by name or type.
    Usage: GET /api/search/?q=pump
    """
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

    results = Equipment.objects.filter(
        equipment_name__icontains=query
    ) | Equipment.objects.filter(
        equipment_type__icontains=query
    )

    serializer = EquipmentSerializer(results, many=True)
    return Response({"count": results.count(), "results": serializer.data}) 
@api_view(['GET'])
def equipment_stats_by_type(request):
    from django.db.models import Avg, Min, Max
    stats = Equipment.objects.values('equipment_type').annotate(
        avg_flowrate=Avg('flowrate'),
        min_flowrate=Min('flowrate'),
        max_flowrate=Max('flowrate'),
        avg_pressure=Avg('pressure'),
        min_pressure=Min('pressure'),
        max_pressure=Max('pressure'),
        avg_temperature=Avg('temperature'),
        min_temperature=Min('temperature'),
        max_temperature=Max('temperature'),
    )
    return Response(list(stats))