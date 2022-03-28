from flaskweb import db
from flaskweb.models import Disease

def save_disease(**kwargs):
    try:
        disease = Disease(**kwargs) 
        db.session.add(disease)
        db.session.commit()   

        return (True, disease)
    except Exception as e:
        return (False, str(e))