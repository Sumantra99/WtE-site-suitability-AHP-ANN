"""Recompute published tables and optionally fit a new ANN surrogate."""
import argparse, csv, json
from pathlib import Path
import numpy as np
BASE = Path(__file__).resolve().parent
CODES = ['DR','CV','GF','DW','LN','ES','HD','LC','DD','AI']
def read(name):
    with (BASE/'data'/name).open() as f:
        return list(csv.DictReader(f))
def score(q, weights):
    q, weights = np.asarray(q, dtype=float), np.asarray(weights, dtype=float)
    if weights.shape != (10,) or not np.isfinite(weights).all() or (weights < 0).any() or weights.sum() <= 0:
        raise ValueError('Ten finite nonnegative weights with positive total required')
    if q.ndim != 2 or q.shape[1] != 10 or not np.isfinite(q).all() or (q < .1).any() or (q > .9).any():
        raise ValueError('Subindices must be finite, with ten columns in [0.1, 0.9]')
    return q @ (weights/weights.sum())
def ahp(matrix):
    a = np.asarray(matrix, dtype=float)
    if a.shape != (3,3) or not np.isfinite(a).all() or (a <= 0).any() or not np.allclose(a*a.T,1):
        raise ValueError('Positive reciprocal 3 by 3 matrix required')
    values, vectors = np.linalg.eig(a)
    k = np.argmax(values.real)
    weights = np.abs(vectors[:,k].real); weights /= weights.sum()
    return weights, float(max(0,(values[k].real-3)/2/.58))
def metrics(y, pred):
    y,pred = np.asarray(y), np.asarray(pred)
    error=y-pred; sse=float(error@error); centered=float(((y-y.mean())**2).sum())
    return dict(RMSE=float(np.sqrt(np.mean(error**2))), MAE=float(np.mean(np.abs(error))),
                NSE=1-sse/centered if centered else None,
                PBIAS=float(100*error.sum()/y.sum()) if y.sum() else None,
                RSR=float(np.sqrt(sse/centered)) if centered else None,
                covariance=float(np.cov(y,pred,ddof=1)[0,1]))
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--train-ann',action='store_true'); args=parser.parse_args()
    out=BASE/'results';out.mkdir(exist_ok=True)
    weights=np.array([float(r['reported_weight']) for r in read('weights.csv')])
    rows=read('site_subindices.csv'); q=np.array([[float(r[c]) for c in CODES] for r in rows])
    si=score(q,weights); published=[float(r['reported_SI']) for r in read('reported_scores.csv')]
    order=np.argsort(-si); ranks={int(i):j+1 for j,i in enumerate(order)}
    with (out/'site_ranking.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['site','recomputed_SI','reported_SI','difference','rank'])
        writer.writerows([[rows[i]['site'],si[i],published[i],si[i]-published[i],ranks[i]] for i in range(4)])
    cw,cr=ahp([[1,3,7],[1/3,1,5],[1/7,1/5,1]])
    summary={'weight_sum':float(weights.sum()),'criteria_eigenvector':cw.tolist(),'criteria_CR_RI_0_58':cr,
             'ranking':[rows[i]['site'] for i in order], 'ann_rows_transcribed':len(read('report_ann_rows.csv')),
             'caution':'Table 8 scores reproduce published SI to rounding precision. Raw-to-Q mapping is unresolved.'}
    source=read('report_ann_rows.csv')
    if source:
        summary['published_ANN_rows_metrics']=metrics([float(r['reported_target']) for r in source],[float(r['reported_prediction']) for r in source])
    if args.train_ann:
        from sklearn.neural_network import MLPRegressor
        from sklearn.linear_model import LinearRegression
        from sklearn.model_selection import train_test_split
        rng=np.random.default_rng(42); x=rng.integers(1,10,size=(4000,10))/10; y=score(x,weights)
        xtrain,xrest,ytrain,yrest=train_test_split(x,y,test_size=.3,random_state=42)
        xval,xtest,yval,ytest=train_test_split(xrest,yrest,test_size=.5,random_state=42)
        candidates=[]
        for alpha in [.00001,.001,.1]:
            net=MLPRegressor(hidden_layer_sizes=(5,),activation='tanh',solver='lbfgs',max_iter=2000,alpha=alpha,random_state=42)
            net.fit(xtrain,ytrain); candidates.append((np.mean((net.predict(xval)-yval)**2),net,alpha))
        _,net,alpha=min(candidates,key=lambda t:t[0])
        baseline=LinearRegression().fit(xtrain,ytrain)
        summary['new_synthetic_surrogate']={'split':[len(xtrain),len(xval),len(xtest)],'selected_alpha':alpha,
            'ANN_test':metrics(ytest,net.predict(xtest)), 'linear_baseline_test':metrics(ytest,baseline.predict(xtest)),
            'note':'New synthetic experiment, not original MATLAB model or independent field validation.'}
        with (out/'new_ann_test_predictions.csv').open('w',newline='') as f:
            writer=csv.writer(f);writer.writerow(['formula_target','ANN_prediction','linear_prediction'])
            writer.writerows(zip(ytest,net.predict(xtest),baseline.predict(xtest)))
    (out/'audit.json').write_text(json.dumps(summary,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4.5)); x=np.arange(4)
    ax.bar(x-.18,si,.36,label='Recomputed from Table 8'); ax.bar(x+.18,published,.36,label='Reported SI')
    ax.set_xticks(x,[r['site'] for r in rows]); ax.set_ylabel('Suitability index');ax.set_ylim(0,.9);ax.legend()
    fig.tight_layout();fig.savefig(out/'site_comparison.png',dpi=160);plt.close(fig)
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
