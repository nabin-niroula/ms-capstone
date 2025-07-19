import pytest
# import file here
import numpy as np
import json
#import os
import sys
sys.path.append('../model')
import model

benign_data = {
	"SourceIP": "0.0.0.0", 
	"DestinationIP": "0.0.0.0", 
	"SourcePort": 12, 
	"DestinationPort": 24, 
	"Duration": 12.4124, 
	"FlowBytesSent": 125, 
	"FlowSentRate": 8692.12, 
    "FlowBytesReceived": 515, 
    "FlowReceivedRate": 515.523,
    "PacketLengthMean": 515.523, 
    "PacketTimeMean": 515.523, 
    "ResponseTimeTimeMean": 515.523, 
    "DoH": True
}

mal_data = {
	"SourceIP": "192.168.20.212", 
	"DestinationIP": "9.9.9.11", 
	"SourcePort": 54066, 
	"DestinationPort": 443, 
	"Duration": 34.0556, 
	"FlowBytesSent": 1875, 
	"FlowSentRate": 55.0571, 
    "FlowBytesReceived": 4964, 
    "FlowReceivedRate": 145.762,
    "PacketLengthMean": 213.719, 
    "PacketTimeMean": 7.86213, 
    "ResponseTimeTimeMean": 0.0098586, 
    "DoH": True
}

wrong_data = {
	"SourceIP": 192, 
	"DestinationIP": "9.9.9.11", 
	"SourcePort": 54066, 
	"DestinationPort": 443, 
	"Duration": 34.0556, 
	"FlowBytesSent": 1875, 
	"FlowSentRate": 55.0571, 
    "FlowBytesReceived": 4964, 
    "FlowReceivedRate": 145.762,
    "PacketLengthMean": 213.719, 
    "PacketTimeMean": 7.86213, 
    "ResponseTimeTimeMean": 0.0098586, 
    "DoH": True
}

cluster_wrong_format1 = {
    "logs": np.random.rand(3, 2).tolist()
}
cluster_wrong_format2 = {
    "logs": 'string input'
}
cluster_correct_format = {
    "logs": np.random.rand(3, 10).tolist()
}


@pytest.fixture
def client():
    model.app.config['TESTING'] = True
    with model.app.test_client() as client:
        yield client


def test_forward(client):
    """[summary: test baseline model forward pass]
        Args: client ([type: class]): [description: Flask test client]
    """
    # correct input format
    URL = '/predict'
    TYPE = 'application/json'
    response = client.post(URL, 
                           data=json.dumps(benign_data),
                           content_type=TYPE)
    assert response.status_code == 200
    response = client.post(URL, 
                           data=json.dumps(mal_data),
                           content_type=TYPE)
    assert response.status_code == 200
    # wrong data type
    response = client.post(URL, 
                        data=json.dumps(wrong_data),
                        content_type=TYPE)
    assert response.status_code == 403
    # no input
    response = client.post(URL)
    assert response.status_code == 403
    
    
def test_cluster(client):
    """[summary: test cluster model fit]
        Args: client ([type: class]): [description: Flask test client]
    """
    # correct input format
    URL = '/cluster'
    TYPE = 'application/json'
    response = client.post(URL, 
                           data=json.dumps(cluster_correct_format),
                           content_type=TYPE)
    assert response.status_code == 200
    # wrong data type
    response = client.post(URL, 
                        data=json.dumps(cluster_wrong_format1),
                        content_type=TYPE)
    assert response.status_code == 403
    # no input
    response = client.post(URL, 
                        data=json.dumps(cluster_wrong_format2),
                        content_type=TYPE)
    assert response.status_code == 403