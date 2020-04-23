# Indicator Functions using cython (v0.0.1)
@Author <>-------<> epociask <>-----------<>
## Still in infancy will require a good amount of work
## Currently only provide support for SMA, Upper Fibonnaci Retracement Levels, && Bollinger Bands (Many to come and many to be ported over from original python)

## To Intall/Run (For Now)

### Add to python envrionment (PIP) 
1. ``` pip3 install -i https://test.pypi.org/simple/ epociask==0.0.1 ```

### Add to python envrionment (Manual)
1. ``` git clone https://github.com/epociask/cython_indicator_functions.git ```
2. ``` python3 setup.py build ``` 
3. ``` python3 setup.py install --user ```


## To Run (For Now)

```python

import indicators

closes = [12.3, 11.5, 23.5, 24.2, 32.4]

print(indicators.SMA(closes, 4))
```
>22.9
```

```
