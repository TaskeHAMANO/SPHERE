functions{
    real inv_trans_sin2(real theta, real mu, real nu){
        real t ;
        t = theta ;
        for (i in 1:8){
            t = t - ((t + nu*pow(sin(t-mu),2) - theta) / (1 + 2 * nu * sin(t-mu) * cos(t-mu))) ;
        }
        return t ;
    }

    real cardioid_lpdf(real theta, real mu, real rho){
        return log(1 + 2 * rho * cos(theta - mu)) - log(2) - log(pi())   ;
    }

    real invmiaecardioid_mixture_lpdf(real R, int K, vector a, vector mu, vector rho, vector nu) {
        vector[K] lp;
        for (k in 1:K){
            lp[k] = log(a[k]) + cardioid_lpdf(inv_trans_sin2(R, mu[k], nu[k]) | mu[k], rho[k]) ;
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
}

transformed data {
    real<lower=-pi(), upper=pi()> RADIAN[I] ;
    vector<lower=0.0>[K] A ; //hyperparameter for dirichlet distribution

    for (i in 1:I){
        RADIAN[i] = -pi() + (2.0 * pi() / L) * (LOCATION[i] - 1) ;
    }
    for (k in 1:K){
        A[k] = 50 / k ;
    }
}

parameters {
    simplex[K] alpha ;
    unit_vector[2] O[K] ;
    vector<lower=0.0, upper=0.5>[K] rho[S] ;
    // skewness parameter
    vector<lower=-1.0, upper=1.0>[K] nu[S] ;
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
        rho[s] ~ student_t(2.5, 0, 0.17) ;
    }
    for(i in 1:I){
        target += DEPTH[i] * invmiaecardioid_mixture_lpdf(RADIAN[i] | K, alpha, ori, rho[SUBJECT[i]], nu[SUBJECT[i]]) ;
    }
}

generated quantities {
    vector<lower=0.0>[K] kappa[S] ;
    vector<lower=1.0>[K] PTR[S] ;
    vector<lower=1.0>[S] mPTR ;
    vector<lower=1.0>[S] wmPTR ;
    vector[I] log_lik ;

    for(s in 1:S){
        // See (Jones&Pewsey, 2005) about this transformation
        kappa[s] = atanh(2 * rho[s]) ;
        // Fold change of max p.d.f. to min p.d.f.
        PTR[s] = exp(2 * kappa[s]) ;
        mPTR[s] = sum(PTR[s] ./ K) ;
        wmPTR[s] = sum(PTR[s] .* alpha) ;
    }
    for(i in 1:I){
        log_lik[i] = DEPTH[i] * invmiaecardioid_mixture_lpdf(RADIAN[i] | K, alpha, ori, rho[SUBJECT[i]], nu[SUBJECT[i]]) ;
    }
}
