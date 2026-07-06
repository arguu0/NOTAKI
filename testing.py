list = [
  {
    "email": "string@gmail.com",
    "password": "$argon2id$v=19$m=65536,t=3,p=4$XSMrPOGfZ5Apx0Ue60sIVQ$iW2xkXM5yDeqeimqOCVmk4VbhV17BZqCuvUhQn7gITY"
  },
  {
    "email": "admin@gmail.com",
    "password": "$argon2id$v=19$m=65536,t=3,p=4$Vrv9RYGABTK3FHRi8EFSOQ$sT6dRr2wtPOJkitf8V2oWk2nnq/5c2WZpJ0xQarbIXc"
  }
]


for i in list:
    if i['email'] == "admin@gmail.com":
        print(i)