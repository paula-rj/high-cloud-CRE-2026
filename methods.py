import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
import xarray as xa

ymonthslist = [
    "Year",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

def anomaly(ds):
    """Computes an anomaly by extracting the monthly climatology.

    Parameters:
    ----------
    ds: xr.Dataset
        Dataset containing a time dimension.
    """
    ds_anom = ds.groupby("time.month") - ds.groupby("time.month").mean("time")
    return ds_anom


def netCRE(lwds, swds, times=False, cc=None):
    """Calculates a net CRE kernel.
    If times, calculates Net CRE (or cloud-induced radiative anomaly R)

    Parameters:
    ----------
    lwds: xr.Dataset
        Dataset containing long-wave TOA rad values. Must be trimmed
    swds: xr.Dataset
        Dataset containing short-wave TOA rad values. Must be trimmed.
    times: bool
        Whether it will be timed by cloud area or fraction
    cc: xr.Dataset
        Cloud cover (The weights.)

    Returns:
    -------
    Kernel (xr.Dataset)
    """
    lw_cre = lwds.toa_lw_clr_mon.mean("lon") - lwds.toa_lw_cldtyp_mon.mean("lon")
    sw_cre = swds.toa_sw_clr_mon.mean("lon") - swds.toa_sw_cldtyp_mon.mean("lon")
    K_trop = (lw_cre + sw_cre) / 100

    if times:
        cc_anom = anomaly(cc)
        return K_trop * cc_anom
    else:
        return K_trop


def recentre(gmst, as_pd=False):
    """ "Returns re-centred array to the period of interest.
    Parametres:
    ----------
    gmst: pandas.Dataframe
        dataset Gistemp GMST anomalies, years already filtered
    as_pd: bool
        Returns corregido as pandas Dataframe.
        Default:False (returns as numpy.Array)

    Returns:
    -------
    recentred: pandas.DataArray
        Recentred values
    """

    gmst = gmst.loc[
        :,
        ymonthslist,
    ]

    months = gmst.columns.to_list()[1:]
    for i in months:
        gmst[i] = gmst[i].astype("float16")

    lista_gmst = gmst[ymonthslist[1:]].values.flatten().tolist()
    gmst_anom_raghu = np.array(lista_gmst[6:], dtype=np.float16)
    # Mean value
    mean_value = np.mean(gmst_anom_raghu)
    df_recentred = gmst[months] - mean_value
    df_recentred.insert(loc=0, column="Year", value=gmst["Year"])

    if as_pd:
        return df_recentred
    else:
        recentred = gmst_anom_raghu - mean_value
        return recentred


def K(wave, Rfull):
    """Computes radiative Kernel.
    wave: str
        sw or lw"""
    if wave not in ["sw", "lw"]:
        raise ValueError(f"wave can only be sw or lw (str). It's {wave}")

    # Compute Kernefu
    Rclr = Rfull[f"toa_{wave}_clr_mon"].mean("lon")
    Rovc = Rfull[f"toa_{wave}_cldtyp_mon"].mean("lon")
    K = (Rclr - Rovc) / 100

    return K


def Rmean_anom(cc, K):
    """Computes mean radiative anomaly. All parameters must have area and time already selected.
    Parameters:
    ----------
    cc: xa.DataSet
        cloud cover (or fraction, or area)
    K: xa.DataSet
        radiative kernel. Can be sw, lw or net

    Returns:
    -------
    R_mean: xa.DataSet
        Radiative anomaly.
    """
    # Compute cloud cover anomaly
    area = cc.mean("lon")
    cc_anom = anomaly(area)

    # Compute radiative anomaly
    R_anom = K.mean("time") * cc_anom

    return R_anom.mean("lat")


def new_pvals(ds, indep, lag):
    """Effective degrees of freedom, given the residuals."""

    new_pvals = np.zeros([len(ds.press.data), len(ds.opt.data)])

    residuos = ds.sel(indep=indep).res.data - np.mean(ds.sel(indep=indep).res.data)

    for od in ds.opt.data.tolist():
        for p in ds.press.data.tolist():

            # Cortamos el array para lag 1
            r_t = residuos[p - ds.press.data[0], od, lag:]  # shape = time.len - 1
            r_tm = residuos[p - ds.press.data[0], od, :-lag]  # shape = time.len - 1

            rho = np.corrcoef(r_t, r_tm)[0, lag]

            Neff = (ds.time.shape[0] * (1 - rho)) / (1 + rho)

            params = ds.slopes.sel(indep=indep, press=p, opt=od)
            std_err = ds.stderr.sel(indep=indep, press=p, opt=od)
            tval = params / std_err

            # New pvals assuming 2-tailored residual distribution
            new_pvals[p - ds.press.data[0], od] = 2 * (
                1 - stats.t.cdf(np.abs(tval), df=Neff)
            )

    return new_pvals

def Neff(resid,lag=1):
    """Calculatres effective degrees of freedom from residuals"""
    r_t = resid[lag:]  # shape = time.len - 1
    r_tm = resid[:-lag]  # shape = time.len - 1
    rho = np.corrcoef(r_t, r_tm)[0, lag]
    Neff = (resid.shape[0] * (1 - rho)) / (1 + rho)
    return Neff


def total_hc(dsregress, var=0):
    tcrit = t.ppf(0.975, df=dsregress.time.shape ) #df=Neff(dsregress.res)
    total = dsregress.sel(press=[4,5,6], indep=var).slopes.sum(["press", "opt"]).data.item()
    ci = dsregress.sel(press=[4,5,6], indep=var).stderr.sum(["press", "opt"]).data.item()
    return total, tcrit*ci
#df=Neff(dsregress.sel(press=[4,5,6], indep=var).res) )
    
def deriv(R_mean, indep):
    """
    Returns (multi)linear regression parameters and stats.

    Parameters:
    ----------
    R_mean: xa.DataSet
        Radiative mean anomaly
    indep: List
        List containing independent variables eg [gmst, aod, sst]

    Returns:
    -------
    ds: xa.DataSet
        Result of the regression with a bunch of statistics.

    Notes:
    -----
    Works for only high clouds but not for reduced dimensions of optical depth.
    """

    X = [ti.astype("float32") for ti in indep]
    multi_dim = len(X)
    X = tuple(X)
    exo = np.column_stack(X)
    # Gets dimentions
    optdim = [int(i) for i in R_mean.opt.data.tolist()]
    pressdim = [int(i) for i in R_mean.press.data.tolist()]

    # Creates arrays to store, 3rd dim is the amount of independet variables in the regression
    R_t = np.zeros([len(pressdim), len(optdim), len(R_mean.time.data)])
    lw_feed_slope = np.zeros([len(pressdim), len(optdim), multi_dim])
    lw_feed_st = np.zeros([len(pressdim), len(optdim), multi_dim])
    p_vals = np.zeros([len(pressdim), len(optdim), multi_dim])
    R_adj = np.zeros([len(pressdim), len(optdim)])
    DWautocorr = np.zeros([len(pressdim), len(optdim)])
    res = np.zeros([len(pressdim), len(optdim), len(R_mean.time.data)])

    for od in optdim:
        for p in pressdim:
            # Selects p and od of interest
            bint = R_mean.sel(press=p, opt=od)
            R_t[p - pressdim[0], od, :] = bint
            # lw_regress = stats.linregress(corregido, bint)
            lw_regress = sm.OLS(bint.data, exo).fit()  # (Multi)Linear regresstion
            lw_feed_slope[p - pressdim[0], od, :] = lw_regress.params.tolist()  # .slope
            lw_feed_st[p - pressdim[0], od, :] = lw_regress.bse.tolist()  # .stderr
            p_vals[p - pressdim[0], od, :] = [
                round(p, 4) for p in lw_regress.pvalues.tolist()
            ]  # p-values
            R_adj[p - pressdim[0], od] = round(
                lw_regress.rsquared_adj, 2
            )  # R2 adjusted
            DWautocorr[p - pressdim[0], od] = round(
                durbin_watson(lw_regress.resid).item(), 2
            )  # Durbin watson coefficients
            res[p - pressdim[0], od] = lw_regress.resid  # residuals [p, od, time]

    ds = xa.Dataset(
        data_vars=dict(
            slopes=(["press", "opt", "indep"], lw_feed_slope),
            stderr=(["press", "opt", "indep"], lw_feed_st),
            p_values=(["press", "opt", "indep"], p_vals),
            R2_adj=(["press", "opt"], R_adj),
            res=(["press", "opt", "time"], res),
            DWautocorr=(["press", "opt"], DWautocorr),
            R_mean=(["press", "opt", "time"], R_t),
            vars=(["indep", "time"]),
        ),
        coords=dict(
            press=pressdim,
            opt=optdim,
            indep=np.arange(multi_dim),
            time=R_mean.time.data,
        ),
    )

    return ds


def decompos_hc(wave, allradds, dates, exog, var=0, p_adj=True, lag=1):

    tcrit = t.ppf(0.975, df=allradds[0].time.shape[0] - len(exog))

    # Retrieves cloud cover, mean across lon
    cc = allradds[0].cldarea_cldtyp_mon.sel(time=dates).mean("lon")

    # Calculates kernels
    if wave == "net":
        K_cc = prueba.K( #means lon
            "sw", allradds[0].sel(time=dates)) + prueba.K("lw", allradds[1].sel(time=dates))
    else:
        K_cc = prueba.K(wave, allradds[0].sel(time=dates),)
    
    cc_anom = prueba.anomaly(cc)  #Cloud cover anomaly
    cTot = cc.sum(["press", "opt"]) #Cloud cover total = adding up all bins
    cTot_anom = cc_anom.sum(["press", "opt"]) #Cloud cover anomaly total
    cc_ast = cc_anom - (cc / cTot) * cTot_anom #Weighted cc

    #Amount
    K_0_hc = (((cc / cTot)) * K_cc).sum(["opt", "press"]) #K0
    Ramt_anom = K_0_hc * cTot_anom #Amount radiative anomaly 
    y = Ramt_anom.mean("lat").data #Area (lat) mean
    #print(y.shape, exog.shape)
    feed_amount = sm.OLS(endog=y, exog=exog).fit() #Regression with all independent variables
    
    if p_adj:
        tcrit = t.ppf(0.975, df=Neff(feed_amount.resid, lag=1))
    f_amt = feed_amount.params[var]
    ci_amt = tcrit * feed_amount.bse[var]
    
    #Altitude
    ct_Tot = (cc / cTot).sum("press")
    Kp = K_cc * ct_Tot.sum("opt")
    K_prima_p = (Kp * ct_Tot).sum("opt")
    almost_R = K_prima_p * cc_ast.sum("opt")
    R_altitude = almost_R.sum("press")
    feed_alt = sm.OLS(endog=R_altitude.mean("lat").data, exog=exog).fit()
    if p_adj:
        tcrit = t.ppf(0.975, df=Neff(feed_alt.resid, lag=1))
    f_alt = feed_alt.params[var]
    ci_alt = tcrit * feed_alt.bse[var]

    #Optical depth
    cp_Tot = (cc / cTot).sum("opt")
    Ktau = K_cc * cp_Tot.sum("press")
    K_prima_tau = (Ktau * cp_Tot).sum("press")
    casi_R = K_prima_tau * cc_ast.sum("press")
    R_od = casi_R.sum("opt")
    feed_od = sm.OLS(endog=R_od.mean("lat").data, exog=exog).fit() 
    if p_adj:
        tcrit = t.ppf(0.975, df=Neff(feed_od.resid, lag=1))
    f_tau = feed_od.params[var]
    ci_tau = tcrit * feed_od.bse[var]

    #Residual
    k_R = K_cc - K_prima_p - K_prima_tau
    R_res = (k_R * cc_ast).sum(["press", "opt"])
    feed_res = sm.OLS(endog=R_res.mean("lat").data, exog=exog).fit() 

    if p_adj:
        tcrit = t.ppf(0.975, df=Neff(feed_res.resid, lag=1))
    f_res = feed_res.params[var]
    ci_res = tcrit * feed_res.bse[var]

    decompos = pd.DataFrame({"what":["Amt", "Alt","OptD", "Res" ],
                            'feed': [f_amt, f_alt, f_tau, f_res, ],
                            'ci': [ci_amt, ci_alt, ci_tau, ci_res, ]},
                             )
   
    #print(decompos)
    return decompos

def main(
    wave,
    allradds,
    dates,
    gmst_np, 
    ml_reg=None,
    noenso=False,
    ranges_to_exclude=[("2015-06-01", "2016-02-01"), ],
):
    """Integrating all processes.
    wave: str
      sw, lw or net
    allradds: xa.DataSet
        alllw or allsw
    dates: slice
        Selected dates
    gmst = pd.DataFrame
        gmst re-centred and already filtered as numpy array
    ml_reg: list od xa.Dataset
        Independent variables. Must be [indep1, indep2, ...]. Must have time dimension. 
    no enso: bool
        True if want to
    if wave == "net":
        K_area = prueba.K(
            "sw", allradds[0].sel(time=dates)) + prueba.K("lw", allradds[1].sel(time=dates))
    else:
        K_area = 
    if wave == "net":
        K_area = prueba.K(
            "sw", allradds[0].sel(time=dates)) + prueba.K("lw", allradds[1].sel(time=dates))
    else:
        K_area = prueba.K(wave, allradds[0].sel(time=dates),)
    """
    if wave not in ["net", "sw", "lw"]:
        raise ValueError(f"wave can only be sw or lw (str). It's {wave}")
    
    # Calculates kernels
    if wave == "net":
        K_area = prueba.K(
            "sw", allradds[0].sel(time=dates)) + prueba.K("lw", allradds[1].sel(time=dates))
    else:
        K_area = prueba.K(wave, allradds[0].sel(time=dates),)
    
    #Calculates radiative anomaly
    R_area_mean = prueba.Rmean_anom(allradds[0].cldarea_cldtyp_mon.sel(time=dates), K_area)

    X = [gmst_np,]

    # In  case of multilinear regression, adds variables toghether
    if ml_reg is not None:
        X.extend(ml_reg)

    if noenso:
        lsnp = [
            (
                np.datetime64(ranges_to_exclude[i][0][:8]+"15", "ms"),
                np.datetime64(ranges_to_exclude[i][1][:8]+"15", "ms"),
            )
            for i in np.arange(len(ranges_to_exclude))
        ]

        filtered_dates = prueba.exclude_dates(allradds[0].sel(time=dates).time.data, exclude_s=lsnp)
        
        R_area_mean = R_area_mean.sel(time=filtered_dates)

        #X = [gmst_np,]

        if ml_reg is not None:
            filtered_indep = [indep.sel(time=filtered_dates) for indep in ml_reg]
            X.extend(filtered_indep)

    #print(f"gmst = {X[0].data.shape}, aod={X[1].data.shape},R={R_area_mean.data.shape}")
     
    ds = prueba.deriv(R_area_mean, X) 

    return ds
