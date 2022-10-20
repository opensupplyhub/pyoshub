import pytest
import pyoshub.pyoshub as pyoshub 
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [
            ('authorization', 'HIDDEN')],
        "record_mode":'new',
        "ignore_localhost":True
    }

@pytest.mark.vcr()
class Test___init__:

    #@pytest.mark.vcr()
    def test_invalid_protocol(self):
        osh_api = pyoshub.OSH_API(url="invalid://will_raise_exception")
        assert(osh_api.result == {'code': -1, 'message': "No connection adapters were found for 'invalid://will_raise_exception/health-check/'"})
        assert(osh_api.error == True)

    #@pytest.mark.vcr()
    def test_invalid_url(self):
        osh_api = pyoshub.OSH_API(url="https://doesnot.ex.ist")
        assert(osh_api.result["code"] == -1)
        assert("Max retries exceeded with url: /health-check/" in osh_api.result["message"])
        assert(osh_api.error == True)

    #@pytest.mark.vcr()
    def test_valid_url(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"])
        assert(osh_api.result["code"] == 0)
        assert(osh_api.result["message"] == "ok")
        assert(osh_api.error == False)

    #@pytest.mark.vcr()
    def test_valid_url(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"])
        assert(osh_api.result["code"] == 0)
        assert(osh_api.result["message"] == "ok")
        assert(osh_api.error == False)


    def test_valid_url_no_token_test_token(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],check_token=True)
        assert(osh_api.result["code"] == -1)
        assert(osh_api.result["message"] == "No/empty token")
        assert(osh_api.error == True)


    def test_valid_url_invalid_token(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token="invalid")
        assert(osh_api.result["code"] == 0)
        assert(osh_api.result["message"] == "ok")
        assert(osh_api.error == False)


    def test_valid_url_invalid_token_test_token(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token="invalid",check_token=True)
        assert(osh_api.result["code"] == 401)
        assert(osh_api.result["message"] == "<Response [401]>")
        assert(osh_api.error == True)


    def test_valid_url_valid_token_test_token(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        assert(osh_api.result["code"] == 0)
        assert(osh_api.result["message"] == "ok")
        assert(osh_api.error == False)


    def test_dotenv(self):
        import yaml
        import os
        yaml_content = {
            "OSH_URL": os.environ["TEST_OSH_URL"],
            "OSH_TOKEN": os.environ["TEST_OSH_TOKEN"]
        }
        with open(".env.yml","w+t") as f:
            f.write(yaml.dump(yaml_content))
        osh_api = pyoshub.OSH_API(check_token=True)
        assert(osh_api.result["code"] == 0)
        assert(osh_api.result["message"] == "ok")
        assert(osh_api.error == False)
        os.remove(".env.yml")


    def test_dotenv_with_path(self):
        import yaml
        import os
        yaml_content = {
            "OSH_URL": os.environ["TEST_OSH_URL"],
            "OSH_TOKEN": os.environ["TEST_OSH_TOKEN"]
        }
        with open("some.filename.yaml","w+t") as f:
            f.write(yaml.dump(yaml_content))
        osh_api = pyoshub.OSH_API(path_to_env_yml="some.filename.yaml",check_token=True)
        assert(osh_api.result["code"] == 0)
        assert(osh_api.result["message"] == "ok")
        assert(osh_api.error == False)
        os.remove("some.filename.yaml")


    def test_dotenv_with_invalid_path(self):
        osh_api = pyoshub.OSH_API(path_to_env_yml="/x/y/z/invalid_file",check_token=True)
        #print("code",osh_api.result["code"])
        #print(f'message @{osh_api.result["message"]}@')
        assert(osh_api.result["code"] == -1)
        assert(osh_api.result["message"] == "[Errno 2] No such file or directory: '/x/y/z/invalid_file'")
        assert(osh_api.error == True)



    def test_credentials_via_url(self):
        import yaml
        from threading import Thread
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import requests

        class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                yaml_content = {
                    "OSH_URL": os.environ["TEST_OSH_URL"],
                    "OSH_TOKEN": os.environ["TEST_OSH_TOKEN"]
                    }
                yaml_text = yaml.dump(yaml_content).encode("utf-8")

                self.send_response(200)
                self.end_headers()
                self.wfile.write(yaml_text) #b'Hello, world!')

        class mytempwebserver(Thread):
            def __init__(self,num_calls=1):
                Thread.__init__(self)
                self.num_calls = num_calls

            def run(self):
                httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
                for i in range(self.num_calls):
                    httpd.handle_request()

        #print("yaml_text",yaml_text)
        thread = mytempwebserver()
        thread.start()
        osh_api = pyoshub.OSH_API(url_to_env_yml="http://localhost:8000",check_token=True)
        try: # clean up lockups, the server should shut down after one call
            while True:
                r = requests.get("http://localhost:8000")
                print(r.text)
        except:
            pass
        thread.join()
        #print("code",osh_api.result["code"])
        #print("message",osh_api.result["message"])
        assert(osh_api.result["code"] == 0)
        assert(osh_api.result["message"] == "ok")
        assert(osh_api.error == False)



