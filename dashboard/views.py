from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from . import GenerateHourlyPlan as gp
import json
import io, base64


# Create your views here.

def dashboard(request):
    ## importing Data
    cap = pd.read_excel("files/Activities_adjust.xlsx", sheet_name='Activity Cap')
    ProdMeat = pd.read_excel("files/Activities.xlsx", sheet_name='Products and Meat')
    seq = pd.read_excel("files/Activities.xlsx", sheet_name='Product Seqeunce')
    req = pd.read_excel("files/req wihtout byproducts.xlsx")
    meat = pd.read_excel("files/Meats_adjust_v3.xlsx", sheet_name='Priority Meat Input')  # delected the byproduct,
    meat_hourly = pd.read_excel("files/hourly_meat_input.xlsx", index_col=0)
    hour_priority = {
        6: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1,
        11: 1,
        12: 1,
        13: 1,
        14: 1,
        15: 2,
        16: 2,
        17: 3,
        18: 3,
        19: 4,
        20: 4,
        21: 4,
        22: 4
    }

    ## Data Cleaning
    # Some products have 0 PiecesInBox, these skus are also excluded
    req = req.loc[req["PiecesInBox"] != 0, :]
    # exclude byproduct(just include meat_id in Meat table)
    meat_hourly = meat_hourly.loc[:, list(meat.Meat.values)]
    # combine meat inputs and requirements
    meat_and_req = req.merge(ProdMeat, left_on='itemkey', right_on='FinishedGoodProductCode', how='left')

    meat_pieces_check = gp.meat_pieces_check(ProdMeat, req, meat)
    activity_time_check = gp.activity_time_check(req, hour_priority, cap, seq)

    ## best plan
    method1_adjusting_rate_list = [0.01, 0.03]
    method2_combo_ratio_list = [0.3, 0.7]
    method2_adjusting_rate_list = [0.01]
    result, best_plan = gp.get_best_plan(meat_and_req, meat_hourly, hour_priority, cap, seq, req,
                                      method1_adjusting_rate_list, method2_combo_ratio_list,
                                      method2_adjusting_rate_list)

    json_records = result.reset_index().to_json(orient='records')
    arr = []
    arr = json.loads(json_records)
    result_ = {"columns" : list(result.columns.values),
                "data" : arr
               }
    stdv,plot = gp.hourly_total_position_stdev(best_plan,cap,hour_priority,seq,plot=True)

    # Show OEE Table for the Best Plan
    OEE, OEE_table = gp.EEO_caculation(best_plan, cap, hour_priority, seq)
    OEE_json=OEE_table.droplevel(1, axis=1)
    OEE_json=OEE_json.reset_index().to_json(orient='records')
    OEE_json= json.loads(OEE_json)
    result_OEE_table = {"columns": list(OEE_table.droplevel(1, axis=1).columns.values),
               "OEE_json": OEE_json,
               }

    # Estimated Position Num for Each Activity (Best Plan)
    pos_num_plots = gp.visualize_estimated_position_num(best_plan,cap,hour_priority,seq)

    # More Detailed Analysis
    # Use Method 1 get an hourly plan

    hourly_packaging_plan_method1, requirements_not_complete_method1 = gp.plan_break_down(meat_and_req, meat_hourly,
                                                                                       hour_priority)
    hourly_packaging_plan_method1

    hourly_packaging_plan_method1_json = hourly_packaging_plan_method1
    hourly_packaging_plan_method1_json = hourly_packaging_plan_method1_json.reset_index().to_json(orient='records')
    hourly_packaging_plan_method1_json = json.loads(hourly_packaging_plan_method1_json)
    result_hppm1_table = {"columns": list(hourly_packaging_plan_method1.columns.values),
                        "hourly_packaging_plan_method1_json": hourly_packaging_plan_method1_json,
                        }
    # Adjust hourly plan with given learning rate
    new_plan, new_infeasible_table = gp.adjust_infeasible_plan(hourly_packaging_plan_method1, req, cap, seq, hour_priority,
                                                            adjusting_rate=0.01)

    # Hourly Total Position Num Before Adjustment
    stdv_hour_pos_BA, hour_pos_plot_BA=gp.hourly_total_position_stdev(hourly_packaging_plan_method1, cap, hour_priority, seq, plot=True)

    # Hourly Total Position Num after Adjustment
    stdv_hour_pos_AA, hour_pos_plot_AA = gp.hourly_total_position_stdev(new_plan, cap, hour_priority, seq, plot=True)

    # pos_num_plots=pos_num_plots[0]


    context = {
        "meat_pieces_check":meat_pieces_check,
        "activity_time_check":activity_time_check,
        "result_":result_,
        "plot":plot,
        "pos_num_plots":pos_num_plots,
        "result_OEE_table":result_OEE_table,
        "result_hppm1_table":result_hppm1_table,
        "stdv_hour_pos_BA":stdv_hour_pos_BA,
        "stdv_hour_pos_AA":stdv_hour_pos_AA,
        "hour_pos_plot_BA":hour_pos_plot_BA,
        "hour_pos_plot_AA":hour_pos_plot_AA,
    }
    return render(request, "dashboard/dashboard.html",context)
