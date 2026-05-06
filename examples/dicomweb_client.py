from dicomforge.dicomweb import DicomwebClient, QidoQuery, UrllibDicomwebTransport


transport = UrllibDicomwebTransport(timeout=10)
client = DicomwebClient("https://pacs.example/dicomweb", transport)

query = QidoQuery().patient_id("MRN-123").modality("CT").limit(10)
studies = client.search_studies(query)

for study in studies:
    print(study.get("StudyInstanceUID"), study.get("PatientName"))
