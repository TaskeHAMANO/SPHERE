functions {
    real aevon_mises_lpdf(real theta, real mu, real kappa, real nu){
        return von_mises_lpdf(theta + nu * cos(theta - mu) | mu, kappa) ;
    }

    real aevon_mises_mixture_lpdf(real R, int K, vector a, vector mu, vector kappa, vector nu) {
        vector[K] lp;
        for (k in 1:K){
            lp[k] = log(a[k]) + aevon_mises_lpdf(R | mu[k], kappa[k], nu[k]) ;
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
    vector<lower=0.0>[K] kappa[S] ;
    // skewness parameter
    vector<lower=-1.0, upper=1.0>[K] nu ;
    // standard deviation for horseshoe prior
    vector<lower=0>[K] sigma  ;
    // global shrinkage parameter for horseshue prior
    real<lower=0> tau ;
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
    tau ~ cauchy(0, 1) ;
    sigma ~ cauchy(0, 1) ;
    // skewness parameter is sampled from horseshue prior
    nu ~ normal(0, sigma * tau) ;
    for(s in 1:S){
        kappa[s] ~ gamma(1.5, 3) ;
    }
    for(i in 1:I){
        target += DEPTH[i] * aevon_mises_mixture_lpdf(RADIAN[i] | K, alpha, ori, kappa[SUBJECT[i]], nu) ;
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
        // Fold change of max p.d.f. to min p.d.f.
        PTR[s] = exp(2 * kappa[s]) ;
        mPTR[s] = mean(exp(2.0 * kappa[s] / K)) ;
        wPTR[s] = mean(exp(2.0 * kappa[s] .* alpha)) ;
        // Mean resultant length
        for (k in 1:K){
            MRL[s][k] = modified_bessel_first_kind(1, kappa[s][k]) / modified_bessel_first_kind(0, kappa[s][k]) ;
        }
        // Circular variance
        CV[s] = 1 - MRL[s] ;
        // Circular standard variation
        CSD[s] = sqrt(-2 * log(MRL[s])) ;
    }
    for(i in 1:I){
        log_lik[i] = DEPTH[i] * aevon_mises_mixture_lpdf(RADIAN[i] | K, alpha, ori, kappa[SUBJECT[i]], nu) ;
    }
}
