functions {
    real inv_trans_sin2(real theta, real mu, real nu){
        real t ;
        real ft ;
        real err ;
        int count ;
        count = 0 ;
        // Small nu works with Newton's method
        if (fabs(nu) <= 0.8){
            t = theta ;
            ft = t + nu*pow(sin(t-mu), 2.0) - theta ;
            err = fabs(ft) ;
            while(err > machine_precision()){
                t = t - (ft / (1.0 + 2.0 * nu * sin(t-mu) * cos(t-mu))) ;
                ft = t + nu*pow(sin(t-mu), 2.0) - theta ;
                err = fabs(ft) ;
                count += 1 ;
                if (count >= 30){
                    break ;
                }
            }
        // Large nu only works with illinois method
        }else{
            real t1 ;
            real t2 ;
            real ft1 ;
            real ft2 ;
            t1 = -2.0*pi() ;
            t2 = 2.0*pi() ;
            ft1 = t1 + nu*pow(sin(t1-mu), 2.0) - theta ;
            ft2 = t2 + nu*pow(sin(t2-mu), 2.0) - theta ;
            t = (t1 * ft2 - t2 * ft1) / (ft2 - ft1) ;
            ft = t + nu*pow(sin(t-mu), 2.0) - theta ;
            err = fabs(ft) ;
            while(err > 1e-13){
                if (ft < 0){
                    t1 = t ;
                    ft1 = t1 + nu*pow(sin(t1-mu), 2.0) - theta ;
                    ft2 /= 2.0 ;
                }else{
                    t2 = t ;
                    ft1 /= 2.0 ;
                    ft2 = t2 + nu*pow(sin(t2-mu), 2.0) - theta ;
                }
                t = (t1 * ft2 - t2 * ft1) / (ft2 - ft1) ;
                ft = t + nu*pow(sin(t-mu), 2.0) - theta ;
                err = fabs(ft) ;
                count += 1 ;
                if (count >= 100){
                    break ;
                }
            }
        }
        return t ;
    }

    real invmiaevon_mises_mixture_lpdf(real R, int K, vector a, vector mu, vector kappa, vector nu) {
        vector[K] lp;
        for (k in 1:K){
            lp[k] = log(a[k]) + von_mises_lpdf(inv_trans_sin2(R, mu[k], nu[k]) | mu[k], kappa[k]) ;
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
    vector<lower=-pi(), upper=pi()>[I] RADIAN ;
    vector<lower=0.0>[K] A; //hyperparameter for dirichlet distribution

    RADIAN = -pi() + (2.0 * pi() / L) * (to_vector(LOCATION) - 1) ;
    A = rep_vector(50.0/K, K) ;
}

parameters {
    simplex[K] alpha ;
    unit_vector[2] O[K] ;
    // Unconstrained concentration parameter
    vector[K] kappa_uncon[S] ;
    // skewness parameter
    vector<lower=-1.0, upper=1.0>[K] nu[S] ;
}

transformed parameters{
    vector[K] ori ;
    vector<lower=0.0>[K] kappa[S] ;

    // convert unit vector
    for (k in 1:K){
        ori[k] = atan2(O[k][1], O[k][2]) ;
    }
    // Add upper bound to kappa using alpha (see 'Lower and Upper Bounded Scalar' in Stan manual)
    for (s in 1:S){
        kappa[s] = log(4) ./ (2 * alpha) .* inv_logit(kappa_uncon[s]) ;
    }
}

model {
    alpha ~ dirichlet(A) ;
    for(s in 1:S){
        alpha .* kappa[s] ~ student_t(2.5, 0, 0.2025) ;
        // Jacobian adjustment for parameter transformation (see 'Lower and Upper Bounded Scalar' in Stan manual)
        target += log(log(4) ./ (2 * alpha)) + log_inv_logit(kappa_uncon[s]) + log1m_inv_logit(kappa_uncon[s]) ;
        nu[s] ~ normal(0, 1.0) ;
    }
    for(i in 1:I){
        target += DEPTH[i] * invmiaevon_mises_mixture_lpdf(RADIAN[i] | K, alpha, ori, kappa[SUBJECT[i]], nu[SUBJECT[i]]) ;
    }
}

generated quantities {
    vector<lower=1.0>[K] PTR[S] ;
    vector<lower=1.0>[K] wPTR[S] ;
    vector<lower=1.0>[S] mwPTR ;
    vector[I] log_lik ;
    real log_lik_sum ;

    for(s in 1:S){
        // Fold change of max p.d.f. to min p.d.f.
        PTR[s] = exp(2.0 * kappa[s]) ;
        wPTR[s] = exp(2.0 * alpha .* kappa[s]) ;
        mwPTR[s] = sum(wPTR[s]) ;
    }
    for(i in 1:I){
        log_lik[i] = DEPTH[i] * invmiaevon_mises_mixture_lpdf(RADIAN[i] | K, alpha, ori, kappa[SUBJECT[i]], nu[SUBJECT[i]]) ;
    }
    log_lik_sum = sum(log_lik) ;
}
