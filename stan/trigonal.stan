data {
    int I ;
    int S ;
    int L ;
    int<lower=1, upper=L> LOCATION[I] ;
    int<lower=1, upper=S> SUBJECT[I] ;
    int<lower=0> DEPTH[I] ;
}

parameters {
    unit_vector[2] O ;
    real<lower=0> H[S] ;
    real<lower=0> sigma_H ;
    real flex;
}

transformed parameters{
    real<lower=-pi(), upper=pi()> ori ;
    vector[L] trend[S] ;
    vector<lower=0>[L] lambda[S] ;
    // convert unit vector
    ori = atan2(O[1], O[2]) ;
    for(s in 1:S){
        // trend from replication rate
        for(l in 1:L){
            trend[s, l] = H[s] / 2.0 * (cos(l * 2.0 * pi() / L - ori) + 1.0) ;
        }
        lambda[s] = exp(trend[s] + flex) ;
    }
}

model {
    for(s in 1:S){
        H[s] ~ normal(0, sigma_H) ;
    }
    for(i in 1:I){
        DEPTH[i] ~ poisson(lambda[SUBJECT[i], LOCATION[i]]) ;
    }
}

generated quantities {
    real<lower=1.0> PTR[S] ;
    vector[I] log_lik ;
    for(s in 1:S){
        PTR[s] = exp(H[s]) ;
    }
    for(i in 1:I){
        log_lik[i] = poisson_lpmf(DEPTH[i] | lambda[SUBJECT[i], LOCATION[i]]) ;
    }
}
