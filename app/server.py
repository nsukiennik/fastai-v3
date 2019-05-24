from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO

from fastai import *
from fastai.vision import *


export_file_url = 'https://www.dropbox.com/s/8p84c4893hx726v/export.pkl?dl=1'

export_file_name = 'export.pkl'

classes = ['business', 'law', 'lifestyle', 'rel-pol', 'sports', 'war', 'entertainment', 'misc', 'science', 'tech']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(export_file_url, path/export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        print('success')
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse("Send text data via GET (/getCategory?text=articletext) and see response for result")

# @app.route('/analyze', methods=['POST'])
# async def analyze(request):
#     data = await request.form()
#     print(data)
#     img_bytes = await (data['file'].read())
#     print(img_bytes)
#     #img = open_image(BytesIO(img_bytes))



#request from react
@app.route('/getCategory', methods=['GET', 'POST'])
async def postArticleText(request):
 if request.method == 'GET':
    text = request.query_params['text']
    category = callMLAlgo(text)
    return JSONResponse({'category' : category})


def callMLAlgo(text):
    prediction = learn.predict(text)[0]
    return str(prediction)





if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app=app, host='0.0.0.0', port=5042)
