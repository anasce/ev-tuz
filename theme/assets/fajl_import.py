import anvil.server
import pandas as pd




anvil.server.connect("server_U75BILEYUQBL5QSBOGVWILSW-F5TP27YXF5YKL7EV")


col_names = ["title","ime","category"] 
df = pd.read_csv('anvilPodaciSamoTuzilastva.csv', encoding = "UTF-8",header=None, names=col_names)
rows=[]
for row in df.to_dict('records'):       
     anvil.server.call("import_podataka",art_dict=row)
    
    

