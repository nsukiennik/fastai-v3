from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO

#from fastai import *

from fastai.text import *



# export_file_url = 'https://www.dropbox.com/s/v6cuuvddq73d1e0/export.pkl?raw=1'
export_file_url = 'https://www.dropbox.com/s/eb3we0qoq4rs4gx/export.pkl?dl=1'
export_file_name = 'export.pkl'


path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

def download_file(url, dest):
    if dest.exists(): return
    with aiohttp.ClientSession() as session:
        with session.get(url) as response:
            data = response.read()
            with open(dest, 'wb') as f: f.write(data)

# async def setup_learner():
#     await download_file(export_file_url, path/export_file_name)
#     try:
#         learn = load_learner(path = path, file = export_file_name)
#         return learn

#     except RuntimeError as e:
#         if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
#             print(e)
#             message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
#             raise RuntimeError(message)
#         else:
#             raise

# loop = asyncio.get_event_loop()
# tasks = [asyncio.ensure_future(setup_learner())]
# learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
# loop.close()

@app.route('/')
def index(request):
    
    return HTMLResponse('check the post response for result')


# @app.route('/analyze', methods=['POST'])
# async def analyze(request):
#     data = await request.form()
#     img_bytes = await (data['file'].read())
#     img = open_image(BytesIO(img_bytes))
#     prediction = learn.predict(img)[0]
#     return JSONResponse({'result': str("check the post request for result")})




#request from react
@app.route('/getCategory', methods=['GET', 'POST'])
def postArticleText(request):
    if request.method == 'GET':

        text = request.query_params['text']
        download_file(export_file_url, path/export_file_name)
        learn = load_learner(path = path, file = export_file_name)
        return learn

    #text = 'Can please Nick at least look at fastai inference manuals?'
        #category = "pocky"
    category = learn.predict(text)
    return JSONResponse({'category' : category})



# def callMLAlgo(text):
# #    learn = load_learner(file = 'export_clas.pkl')
#     download_file(export_file_url, path/export_file_name)
#     try:
#          learn = load_learner(path = path, file = export_file_name)
#          return learn
#     except RuntimeError as e:
#              if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
#                  print(e)
#                  message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
#                  raise RuntimeError(message)
#              else:
#                  raise
#     text = 'Can please Nick at least look at fastai inference manuals?'
#     #category = learn.predict(text)
#     category = "pocky"
#     return category


    

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app=app, host='0.0.0.0', port=5042)