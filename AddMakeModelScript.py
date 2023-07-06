import csv

filename = 'input/make_model.csv'
output = 'output/makemodel.sql'
def readData():
    # List of Vins
    # //write_to_csv()
    # //write_to_error_csv()
    text = ["--delete from EVM.dbo.Make where countrycode = 974","--delete from EVM.dbo.Model where countrycode = 974","DECLARE @makeid int","DECLARE @modelid int"]
    mkDict = {}

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        i=0
        prev_make = ""
        for row in datareader:
            # if(i>308057):
            #     processRow(row)
            cur_make = row[0]
            
            if(cur_make != prev_make):
                mknm = row[0]
                mknm = mknm.upper()
                mkcode = 'QA'+mknm[3:4].replace('-','')+mknm[2:3].replace('-','')+mknm[0:1].replace('-','')
                
                text.append("If not exists(Select 1 from EVM.dbo.Make where makecode = '"+mkcode+"')")
                text.append("BEGIN")
                text.append("\tINSERT INTO EVM.dbo.Make(MakeCode,MakeName,MakeUniversalName,DisplayInd,PolkVerfiedInd,SalvageType,NCI_MAK_ABBR_CD,CountryCode)VALUES('"+mkcode+"','"+mknm+"','"+mknm+"' ,  1, 0,'1', '', 974 )")
                text.append("END")
                text.append("SELECT @makeid = makeid FROM EVM.dbo.make WHERE MakeCode = '"+mkcode+"'")
                print(row[0]+',',row[1]+',',mkcode)
            mdnm= row[1]
            mdnm = mdnm.upper()
            mdcode = 'QA'+mdnm.replace('-','')
            text.append("If not exists(Select 1 from EVM.dbo.Model where ModelCode = '"+mdcode+"')")
            text.append("BEGIN")
            text.append("\t INSERT INTO EVM.dbo.Model(ModelCode,ModelName,ModelUniversalName,DisplayInd,PolkVerifiedInd,CountryCode)VALUES( '"+mdcode+"',  '"+mdnm+"',   '"+mdnm+"',   1,  0,   974 )")
            text.append("END")
            text.append("SELECT @modelid = modelid FROM EVM.dbo.model WHERE ModelCode = '"+mdcode+"' ")
            text.append("IF @makeid is not null and @modelid is not null")
            text.append("BEGIN")
            text.append("If not exists(Select 1 from EVM.dbo.MakeModelXRef  with (NOLOCK)  WHERE modelid = @modelid AND makeid = @makeid)")
            text.append("\tBEGIN")
            text.append("\t\tINSERT INTO EVM.dbo.MakeModelXRef(MakeId,ModelId,salvagetype) VALUES( @makeid,@modelid, '1')")
            text.append("\tEND")
            text.append("END")
            prev_make = cur_make
            i = i+1
    writescript(text)

def writescript(text):
    with open(output, 'w') as f:
        for line in text:
            f.write(line)
            f.write('\n')
readData()