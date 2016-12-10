#REST API can be used via the curl shell command
#   curl http://localhost:5001/         or
#   curl http://127.0.0.1:5001/
#   See usage line below each API point
'''
1.  /timeseries GET 
    returns metadata for ALL time series as JSON payload
    Return JSON schema: [{'TSid':stringval, 'TSmean':floatval, 'TSstd':floatval, 'TSblarg':floatval, 'TSlevel':charval,'TSfilepath':stringval}]
    USAGE: curl http://localhost:5001/timeseries

    /timeseries?mean_in=floatfloor-floatceiling
    /timeseries?level=charvalue
    /timeseries?level_in=char1,char2,char3
    /timeseries?fullfilepath=stringval
    Each of these returns metadata for all timeseries that match the selection criteria
    Return JSON schema: [{'TSid':stringval, 'TSmean':floatval, 'TSstd':floatval, 'TSblarg':floatval, 'TSlevel':charval,'TSfilepath':stringval}]
    USAGE:  curl http://localhost:5001/timeseries?mean_in=0.003-12.3265
            curl http://localhost:5001/timeseries?level=D
            curl http://localhost:5001/timeseries?level_in=B,D,F
            curl http://localhost:5001/timeseries?fullfilepath="/usr/tmp/"

2.  /timeseries POST <json payload>
    given a JSON payload,as below, add a timeseries to the database and return a JSON payload with the timeseries
    Input JSON schema: {'TSid':stringval, 'TSfilepath':stringval}
    Return JSON schema: {'Times': [floatvals], 'Values':[floatvals]}
    USAGE: curl -H "Content-type: application/json" -X POST http://localhost:5001/timeseries -d '{"TSid:"idstring", "TSfilepath":"pathstring"}'
    
3.  /timeseries/TSid
    returns metadata and time series for given TSid
    Return JSON schema: {'TSid':stringval, 'TSmean':floatval, 'TSstd':floatval, 'TSblarg':floatval, 'TSlevel':charval,
                         'TSfilepath':stringval, 'Times': [floatvals], 'Values':[floatvals]}
    USAGE: curl http://localhost:5001/timeseries/idstring                   

4.  /simquery/TSid
    returns the top 5 most similar time series to the given TSid. Only the TSids are returned sorted from most similar to less similar
    Return JSON schema: {'SortedSimTS':[TSid vals]}
    USAGE: curl http://localhost:5001/simquery/idstring

5.  /simquery POST <json payload>
    returns the top 5 most similar time series to the given timeseries in the input json payload. Only the TSids are returned sorted from most similar to less similar
    Input JSON schema: {'Times': [floatvals], 'Values':[floatvals]}
    Return JSON schema: {'SortedSimTS':[TSid vals]}
    USAGE curl -H "Content-type: application/json" -X POST http://localhost:5001/simquery -d '{"Times:"[list of times]", "Values":"[list of vals]"}'

'''