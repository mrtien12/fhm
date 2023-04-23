
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
import pandas as pd
import fhm
from io import BytesIO

app = FastAPI()

@app.post("/get_k")
async def get_k(data_customer: UploadFile = File(...), product_data: UploadFile = File(...), threshold_mode: bool = True, percent: float = 0.1, number: int = 1):
    print(f"percent: {percent}")
    print(f"threshold_mode: {threshold_mode}")
    
    transactions = pd.read_csv(BytesIO(await data_customer.read()))
    transactions = transactions.groupby('no').apply(lambda x: [(p,q) for p,q in zip(x['product'],x['quantity'])]).reset_index().values.tolist()
    
    product_df = pd.read_csv(BytesIO(await product_data.read()))
    price = dict(zip(product_df['product'], product_df['price']))
    
    fhm1 = fhm.FHM(transactions, price, percent if threshold_mode else number, minutil_pc=threshold_mode)
    k = fhm1.run_FHM()
    
    return {"k": k}