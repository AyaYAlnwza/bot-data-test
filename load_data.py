from vector_db import init_db, add_document

print("เริ่มรัน load_data.py")  # debug

# สร้าง collection ใหม่
init_db()

# ข้อมูลตัวอย่างใส่ลง database
docs = [
    "สิชลคุณาธารวิทยา ตั้งอยู่ในจังหวัดนครศรีธรรมราช",
    "สภานักเรียน STV SC New Era มีหน้าที่จัดกิจกรรมในโรงเรียน",
    "Python เป็นภาษาที่ง่ายและเหมาะกับผู้เริ่มต้น"
]

for i, d in enumerate(docs):
    add_document(d, i)

print("โหลดข้อมูลเสร็จแล้ว!")
