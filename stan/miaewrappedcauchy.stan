functions{
    real trans_sin2(real theta, real mu, real nu){
        real theta_mu ;
        theta_mu =  theta - nu * sin(theta - mu) * sin(theta - mu) ;
        return theta_mu ;
    }

    real wrappedcauchy_lpdf(real theta, real mu, real rho){
        return log(1 - pow(rho, 2)) - log(2) - log(pi()) - log(1 + pow(rho, 2) - 2 * rho * cos(theta - mu)) ;
    }

    real miaewrappedcauchy_lpdf(real theta, real mu, real rho, real nu){
        return wrappedcauchy_lpdf(trans_sin2(theta, mu, nu)| mu, rho) ;
    }

    real miaewrappedcauchy_normalize_constraint(real mu, real rho, real nu, int N){
        // Numerical integration by composite Simpson's rule
        vector[N+1] lp ;
        real h ;

        h = 2 * pi() / N ;
        lp[1] = miaewrappedcauchy_lpdf(-pi() | mu, rho, nu) ;
        for (n in 1:(N/2)){
            lp[2*n] = log(4) + miaewrappedcauchy_lpdf(-pi() + h*(2*n-1) | mu, rho, nu) ;
        }
        for (n in 1:(N/2-1)){
            lp[2*n+1] = log(2) + miaewrappedcauchy_lpdf(-pi() + h*2*n | mu, rho, nu) ;
        }
        lp[N+1] = miaewrappedcauchy_lpdf(pi() | mu, rho, nu) ;
        return (log(h/3) + log_sum_exp(lp)) ;

    } 

    real miaewrappedcauchy_mixture_lpdf(real R, int K, vector a, vector mu, vector rho, vector nu) {
        vector[K] lp ;
        real logncon ;

        for (k in 1:K){
            logncon = miaewrappedcauchy_normalize_constraint(mu[k], rho[k], nu[k], 20) ;
            lp[k] = log(a[k]) + miaewrappedcauchy_lpdf(R | mu[k], rho[k], nu[k]) - logncon ;
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
    vector[K] rho_uncon[S] ;
    // skewness parameter
    vector<lower=-1.0, upper=1.0>[K] nu[S] ;
}

transformed parameters{
    vector[K] ori ;
    vector<lower=0.0, upper=1.0>[K] rho[S] ;

    // convert unit vector
    for (k in 1:K){
        ori[k] = atan2(O[k][1], O[k][2]) ;
    }
    // Add upper bound to kappa using alpha (see 'Lower and Upper Bounded Scalar' in Stan manual)
    for (s in 1:S){
        for (k in 1:K){
            rho[s][k] = fmin(1.0/3.0/alpha[k], 1.0) .* inv_logit(rho_uncon[s][k]) ;
        }
    }
}

model {
    alpha ~ dirichlet(A) ;
    for(s in 1:S){
        alpha .* rho[s] ~ student_t(2.5, 0, 0.1) ;
        // Jacobian adjustment for parameter transformation (see 'Lower and Upper Bounded Scalar' in Stan manual)
        for (k in 1:K){
            target += log(fmin(1.0/3.0/alpha[k], 1.0)) + log_inv_logit(rho_uncon[s][k]) + log1m_inv_logit(rho_uncon[s][k]) ;
        }
        nu[s] ~ normal(0, 1) ;
    }
    for(i in 1:I){
        target += DEPTH[i] * miaewrappedcauchy_mixture_lpdf(RADIAN[i] | K, alpha, ori, rho[SUBJECT[i]], nu[SUBJECT[i]]) ;
    }
}

generated quantities {
    vector<lower=0.0>[K] kappa[S] ;
    vector<lower=1.0>[K] PTR[S] ;
    vector<lower=1.0>[K] wPTR[S] ;
    vector<lower=1.0>[S] mwPTR ;
    vector<lower=0.0, upper=1.0>[K] MRL[S] ;
    vector<lower=0.0, upper=1.0>[K] CV[S] ;
    vector<lower=0.0>[K] CSD[S] ;
    vector[I] log_lik ;
    real log_lik_sum ;

    for(s in 1:S){
        // See (Jones&Pewsey, 2005) about this transformation
        kappa[s] = 2 * atanh(rho[s]) ;
        // Fold change of max p.d.f. to min p.d.f.
        PTR[s] = exp(2 * kappa[s]) ;
        wPTR[s] = exp(2 * 2 * atanh(alpha .* rho[s])) ;
        mwPTR[s] = sum(wPTR[s]) ;
        // Mean resultant length
        MRL[s] = rho[s] ;
        // Circular variance
        CV[s] = 1 - MRL[s] ;
        // Circular standard variation
        CSD[s] = sqrt(-2 * log(MRL[s])) ;
    }
    for(i in 1:I){
        log_lik[i] = DEPTH[i] * miaewrappedcauchy_mixture_lpdf(RADIAN[i] | K, alpha, ori, rho[SUBJECT[i]], nu[SUBJECT[i]]) ;
    }
    log_lik_sum = sum(log_lik) ;
}
