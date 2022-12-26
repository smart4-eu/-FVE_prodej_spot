import csv
import urllib3
import json
import getopt
import sys

def Load_CEZ_CSV(file):
    Items=[]
    with open(file, 'r', encoding='ANSI') as csvf:
        for line in csv.reader(csvf,delimiter=';'):
            item={}
            DateTime=line[0].split(' ');
            if len(DateTime) >= 2:
                item['Date']=DateTime[0]
                item['Hour']=DateTime[1].split(':')[0]
                item['Minute']=DateTime[1].split(':')[1]
                item['Power_kW']=float(line[1].replace(',', '.'))
                item['Energy_kWh']=float(item['Power_kW'])*0.25 # in Power_kW is the average power in a given quarter-hour
                item['Price_EUR_MW']=0.0
                item['CZK_EUR']=0.0
                Items.append(item)
    return Items

def Update_Price(items,progress=False):
    OldDate=""
    values=[]
    Newitems=[]
    http = urllib3.PoolManager()
    if Progress:
        print("Update price")
    for item in items:
        if OldDate != item['Date']:
            if progress:
                print(f"Date: {item['Date']}")
            Date=item['Date'].split('.');
            Query=f"https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date={Date[2]}-{Date[1]}-{Date[0]}"
            r = http.request("GET",Query)
            values=[]
            if r.status == 200:
                OldDate=item['Date']
                try:
                    data=json.loads(r.data.decode('utf-8'))
                    for value in data['data']['dataLine'][1]['point']:
                        values.append(float(value['y']))
                except:
                    if progress:
                        print("No Data for this day")
                    return Newitems
                    
        if len(values) == 24:
            hour=int(item['Hour'])
            item['Price_EUR_MW']=values[hour]
            Newitems.append(item)
            
    return Newitems

def Update_Rate(items,progress=False):
    OldDate=""
    rate=None
    Newitems=[]
    if progress:
        print("Update rate")
    http = urllib3.PoolManager()
    for item in items:
        if OldDate != item['Date']:
            if progress:
                print(f"Date: {item['Date']}")
            Query=f"https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date={item['Date']}"
            r = http.request("GET",Query)
            rate=None
            if r.status == 200:
                for row in r.data.decode('utf-8').splitlines():
                    columns=row.split('|')
                    if len(columns) == 5:
                        if columns[3] == "EUR":
                            rate=float(columns[4].replace(',', '.'))
                            break
                OldDate=item['Date']
                    
        if rate is not None:
            item['CZK_EUR']=rate
            Newitems.append(item)
            
    return Newitems     
    
if __name__ == "__main__":
    ImportFile="pnd_export.csv"
    ExportFile="out.csv"
    Progress=False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:p", ["input=", "output=", "progress"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
        
    for o, a in opts:
        if o in ("-i", "--input"):
            ImportFile = a
        elif o in ("-o", "--output"):
            ExportFile = a
        elif o in ("-p", "--progress"):
            Progress = True

    Items=Load_CEZ_CSV(ImportFile)
    Items=Update_Price(Items,progress=Progress)
    Items=Update_Rate(Items,progress=Progress)
    #Calculate average price
    SumEnergy=0
    SumMoney=0
    AVGPrice=0
    
    for item in Items:
        SumEnergy=SumEnergy+item['Energy_kWh']                           
        Money=item['Energy_kWh']*item['Price_EUR_MW']*item['CZK_EUR']/1000 # 1000 is for conversion from kWh to MWh
        SumMoney=SumMoney+Money
        
    if SumEnergy > 0:     
        AVGPrice=SumMoney/SumEnergy
 
    print(f"Average price={AVGPrice:.2f} CZK/kWh, Total earned={SumMoney:.2f} CZK, Total Energy={SumEnergy:.2f}")
    
    with open(ExportFile, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, Items[0].keys())
        w.writeheader()
        for  item in Items:
            w.writerow(item)
