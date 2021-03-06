
import numpy as np
import matplotlib.pylab as plt
import Tkinter, Tkconstants, tkFileDialog
import dataReader as dr

tkObj=Tkinter.Tk()
tkObj.file_opt = options = {}
options['defaultextension'] = '.dat'
X=[]
Y=[]
  
a=tkFileDialog.askopenfiles('r')
if a:
    for file in a:
#         print file.name
        data=dr.csvReader(file.name, ',', 4)
#         print data
        header={}
        for i in range(len(data['header'][2])):
            header[data['header'][2][i].strip()]=i
        
        fittsData={'movementTime':[],'error':[],'width':[],'distance':[],'clickX':[],'clickY':[],'wrongClick':[],\
                   'targetX':[],'targetY':[],'dist2Tar':[],'movDistance':[],\
                   'outliers':[]}
        
        
        
        for i in data['data']:
            if fittsData['movementTime']!=[]:
                tempTime=float(i[1])-lastTime
                lastTime=float(i[1])
            else:
                tempTime=float(i[1])
                lastTime=float(i[1])
            fittsData['movementTime'].append(tempTime)
            fittsData['error'].append(float(i[header['errorMargin']]))
            fittsData['width'].append(float(i[header['width']]))
            fittsData['distance'].append(float(i[header['distance']]))
            fittsData['clickX'].append(float(i[header['clickX']]))
            fittsData['clickY'].append(float(i[header['clickY']]))
            fittsData['wrongClick'].append(float(i[header['clicked']]))
            fittsData['targetX'].append(float(i[header['targetX']]))
            fittsData['targetY'].append(float(i[header['targetY']]))
            
        #Effective width calculation
        for i in range(len(fittsData['movementTime'])):
            if fittsData['wrongClick'][i]!=1:
                a=[fittsData['targetX'][i],fittsData['targetY'][i]]
                b=[fittsData['clickX'][i],fittsData['clickY'][i]]
                a=np.array(a)
                b=np.array(b)
                fittsData['dist2Tar'].append(np.linalg.norm(a-b))
                
                if i>0:
                    p=[fittsData['clickX'][i-1],fittsData['clickY'][i-1]]
                    p=np.array(p)
                    fittsData['movDistance'].append(np.linalg.norm(a-p))
                    
                else:
                    fittsData['movDistance'].append(-1)
            else:
                fittsData['movDistance'].append(-1)
            
        we=4.133*np.std(fittsData['dist2Tar'])
        
#         de=np.mean(fittsData['movDistance'])
        de=[fittsData['movDistance'][i] for i in range(len(fittsData['movDistance'])) if fittsData['movDistance'][i]!=-1]
        meanDe=np.mean(de)
        stdDistance=np.std(de)
        
        mvt=[fittsData['movementTime'][i] for i in range(len(fittsData['wrongClick'])) if fittsData['wrongClick'][i]==0]
        meanMvt=np.mean(mvt)
        stdMvt=np.std(mvt)
        
        #Outlier Detection
        outlier=[0 for i in range(len(fittsData['movementTime']))]
        for i in range(len(fittsData['movementTime'])):
            if fittsData['movDistance'][i]!=-1:
                if np.abs(fittsData['movementTime'][i]-meanMvt)>=3*stdMvt or \
                np.abs(fittsData['movDistance'][i]-meanDe)>=3*stdDistance:
                    outlier[i]=1
#                     print(fittsData['movDistance'][i],fittsData['movementTime'][i])
#                     print(meanDe,stdDistance,meanMvt,stdMvt)
                else:
                    outlier[i]=0
            else:
                outlier[i]=1
                
        fittsData['outliers']=outlier
        IDe=[]
        index=[]
        #Fitts law coefficients
        for i in range(len(fittsData['movementTime'])):
            if fittsData['outliers'][i]!=1:
                
                Y.append(fittsData['movementTime'][i]) #array of MT
    #             dist=fittsData['distance'][i]
    #             width=fittsData['width'][i]
                dist=meanDe
                width=we
                
                #1 is added to calculate the intercept
                X.append([1,np.log2(dist/width+1)])
                IDe.append(np.log2(dist/width+1))
                index.append(i)

#         print"IDE"
#         print IDe
#         print"IDE"

    Y=np.array(Y)
    X=np.array(X)
    Xt=np.transpose(X)
    
    c=np.dot(np.dot(np.linalg.inv(np.dot(Xt,X)),Xt),Y)
    print(c)
    IP=1/c[1]
    print('IP %.4f'%(IP))
        

