from base import session, Base

User = Base.classes.user
# Doesn't support hash properly

def login(username, password):
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and user.password_hash == password:
            return user
        else:
            return None
        
    except Exception as e:
        print("Error:", e)
        return None

#user1 = session.query(User).filter_by(Id=3).first()  
#print(user1.Id, user1.username)

'''
ID: 1, Name: Kari Normann, password: fewf43f4gf5g5
ID: 3, Name: Ola Normann, password: fewf43frf43f4gf5g5
ID: 6, Name: Peter Northug, password: grokfo4kok55949
ID: 7, Name: Marit Bjørgen, password: 5434rf43f4gf5g5
ID: 8, Name: Therese Johaug, password: skilover123
ID: 9, Name: Johannes Høsflot Klæbo, password: sprintking456
ID: 10, Name: Martin Johnsrud Sundby, password: skimarathon789
ID: 11, Name: Ingvild Flugstad Østberg, password: crosscountry567
ID: 12, Name: Kari Vikhagen Gjeitnes, password: nordic123
'''

print(login("Kari Normann", "fewf43f4gf5g5"))
print(login("Kari Normann", " "))
print(login("test", "test"))