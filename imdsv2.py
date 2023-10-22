# Copyright 2014. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import requests
import json

def getIMDSv2Token(duration = 3600):
    url = "http://169.254.169.254/latest/api/token"
    headers = {"X-aws-ec2-metadata-token-ttl-seconds": f"{duration}"}

    response = requests.put(url, headers=headers)

    if response.status_code == 200:
        TOKEN = response.text
        return TOKEN
    else:
        print(f"Failed to obtain a token. Status code: {response.status_code}")
        return ""
        
def getEC2RegionIMDSv2():

        TOKEN = getIMDSv2Token()
        url = "http://169.254.169.254/latest/dynamic/instance-identity/document"
        headers = {"X-aws-ec2-metadata-token": TOKEN}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            metadata = json.loads(response.text)
            return metadata['region']
        else:
            print(f"Failed to retrieve metadata. Status code: {response.status_code}")
            return ""