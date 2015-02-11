#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''
#object struct for json
class GPSData_strut(object):
    def __init__(self,  fld=None):
        if not fld:
            self.Date = '20060415'
            self.Time = '150236'
            self.Company = 'H'
            self.Phone = '13510354262'
            self.Longitude = 114.114117
            self.Latitude = 22.550917
            self.speed = 66
            self.Azimuth = 4 #Orientation of 16 equal of circle, the orientation of north is 0, clockwise
            self.Opertaion_status = 0 #0 represents taxi with no passengers, 1represents taxi with passengers
            self.Equipment_status = 0 #The status of equipment, 0 represents unavailable and 1 represents available.
        else :
            equipment_ok = int(fld[9].split(';')[0])
            self.Date = fld[0]
            self.Time = fld[1]
            self.Company = fld[2]
            self.Phone = fld[3]
            if equipment_ok== 1 :
                self.Longitude = float(fld[4])
                self.Latitude = float(fld[5])
                self.speed = int(fld[6])
                self.Azimuth = int(fld[7])
                self.Opertaion_status = int(fld[8])
            self.Equipment_status = equipment_ok
            
def read_trace_by_taxi_id(taxi_id, month = 5, day = 26, hour = 10):
    #fn = _filename % (month, day, hour)
    fn = 'taxidata.txt'
    print 'loading file: %s' % (fn)
    f = open(fn,'r')
    gpslist = []
    iok, ierr = 0,0
    for lines in f :
        fields = lines.split(',')  
        rec = GPSData_strut(fields)
        if  rec.Equipment_status == 1  :
            if rec.Phone == taxi_id :
                gpslist.append(rec)
            iok += 1 
        else :
            ierr += 1   
    f.close()    
    print 'total points without error: %d '  % len(gpslist)
    print 'count %d  and errors %d' %(iok+ierr, ierr)
    return gpslist

if __name__ == "__main__":
    pass # place test code here
