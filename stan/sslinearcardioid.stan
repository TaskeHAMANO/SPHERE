 functions {
    real sslinearcardioid_lpdf(real theta, real mu, real kappa, real lambda){
        return log(1 + 2 * kappa * (fabs(fabs(theta - mu) - pi()) - pi() / 2)) - log(2) -log(pi()) + log(1 + lambda * sin(theta - mu)) ;
    }

    real sslinearcardioid_mixture_lpdf(real R, int K, vector a, vector mu, vector kappa, vector lambda) {
        vector[K] lp;
        for (k in 1:K){
            lp[k] = log(a[k]) + sslinearcardioid_lpdf(R | mu[k], kappa[k], lambda[k]) ;
        }
        return log_sum_exp(lp) ;
    }
}

data {
    int I ;
    int S ;
    int L ;
    int<lower=1, upper=L> LOCATION[I] ;
    int<lower=1, upper=S> SUBJECT[I] ;
    int<lower=0> DEPTH[I] ;
    int<lower=1> K ; // number of mixed distribution
    vector<lower=0.0>[K] A; //hyperparameter for dirichlet distribution
}

transformed data {
    real RADIAN[I] ;
    for (i in 1:I){
        if(i < L/2.0){
            RADIAN[i] = 2.0 * pi() * LOCATION[i] / L ;
        }else{
            RADIAN[i] = 2.0 * pi() * (LOCATION[i] - L) / L ;
        }
    }
}

parameters {
    simplex[K] alpha ;
    unit_vector[2] O[K] ;
    vector<lower=0.0, upper=1/pi()>[K] kappa[S] ;
    vector<lower=-1.0, upper=1.0>[K] lambda[S] ;
}

transformed parameters{
    vector[K] ori ;

    // convert unit vector
    for (k in 1:K){
        ori[k] = atan2(O[k][1], O[k][2]) ;
    }
}

model {
    alpha ~ dirichlet(A) ;
    for(s in 1:S){
        kappa[s] ~ normal(1/pi()/2, 1/pi()/2) ;
        lambda[s] ~ normal(0, 1) ;
    }
    for(i in 1:I){
        target += DEPTH[i] * sslinearcardioid_mixture_lpdf(RADIAN[i]| K, alpha, ori, kappa[SUBJECT[i]], lambda[SUBJECT[i]]) ;
    }
}

generated quantities {
    vector<lower=1.0>[K] PTR[S] ;
    vector<lower=1.0>[S] mPTR ;
    vector<lower=1.0>[S] wPTR ;
    vector<lower=0.0, upper=1.0>[K] MRL[S] ;
    vector<lower=0.0, upper=1.0>[K] CV[S] ;
    vector<lower=0.0>[K] CSD[S] ;
    vector[I] log_lik ;

    for(s in 1:S){
        PTR[s] = (1 + pi() * kappa[s]) ./ (1 - pi() * kappa[s]) ;
        mPTR[s] = mean((1 + pi() * kappa[s] / K)  ./ (1 - pi() * kappa[s] / K)) ;
        wPTR[s] = mean((1 + pi() * kappa[s] .* alpha)  ./ (1 - pi() * kappa[s] .* alpha)) ;
        MRL[s] = kappa[s] ;
        CV[s] = 1 - MRL[s] ;
        CSD[s] = sqrt(-2 * log(kappa[s])) ;
    }
    for(i in 1:I){
        log_lik[i] = DEPTH[i] * sslinearcardioid_mixture_lpdf(RADIAN[i]| K, alpha, ori, kappa[SUBJECT[i]], lambda[SUBJECT[i]]) ;
    }
}
