def writeCsvFile(fname, data, *args, **kwargs):
        import csv
        mycsv = csv.writer(open(fname, 'wb'), *args, **kwargs)
        for row in data:
            mycsv.writerow(row)
