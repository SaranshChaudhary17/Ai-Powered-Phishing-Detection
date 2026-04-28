# Major Project

This project trains and runs a phishing URL detector using your dataset.

## Folder structure

- `data/phishing_site_urls.csv`: your dataset copied from the zip you provided
- `models/`: trained model and metrics output
- `src/url_features.py`: feature engineering for URLs
- `train.py`: model training script
- `predict.py`: single-URL prediction script
- `app.py`: local web server that exposes the trained model through a website
- `web/`: professional frontend for the phishing URL scanner

## How to run

Train the model:

```powershell
python train.py
```

Test a URL after training:

```powershell
python predict.py --url "http://example.com"
```

Run the website and backend server:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:8000
```

If port `8000` is already used by an older server, run:

```powershell
python app.py --port 8010
```

Then open:

```text
http://127.0.0.1:8010
```

The improved project uses a stronger final model:

- expanded handcrafted URL features
- a tuned Random Forest classifier
- a higher default decision threshold (`0.80`) to reduce false positives on normal websites

Append a new URL to the dataset only when the model is confident:

```powershell
python update_dataset.py --url "http://example.com/login"
```

Quick training on a smaller subset:

```powershell
python train.py --sample-size 50000
```
