import os

# def test_rule_engine():

#     from biwt_rule_engine import load_rules_from_csv

#     csv_file = "./bin/biwt_protype_rules.csv"
#     csv_file = os.path.expanduser(csv_file)
#     rules = load_rules_from_csv(csv_file)

#     for r in rules[:5]:
#         print(r)


# def biwt_dev_mode(biwt):

#     try:
#         test_rule_engine()
#     except Exception as e:
#         print(f"[Rule Engine Test] Error: {e}")

    # file_name = "./data/visium_adata.h5ad"
    # file_name = "./data/Zhuang-ABCA-1-1.064_raw_wClusterAnnots.h5ad"
    # file_name "./data/pbmc3k_clustered.h5ad"
    # file_name = "./data/abc/metadata/Zhuang-ABCA-1/20231215/views/cell_metadata_with_cluster_annotation.csv"
    # file_name = "./data/cells.csv"
    # file_name = "/Users/danielbergman/seq-to-ic-test/data_all/inputdata_download.Rds"
    # file_name = "/Users/danielbergman/pdac-ecm/image_data/j1568sobj_2.rds"
    # file_name = "~/seq-to-ic-test/data_all/visium_adata.h5ad"

    # file_name = "/Users/marwanaji/PhysiCell-Studio.git/visium_adata.h5ad"

    # file_name = os.path.expanduser(file_name)
    # print(f"Importing {file_name}")
    # if "Zhuang" in file_name:
    #     biwt.column_line_edit.setText("subclass")
    # elif file_name.lower().endswith(".rds"):
    #     biwt.column_line_edit.setText("celltype")
    # else:
    #     biwt.column_line_edit.setText("cluster")
    # biwt.import_file(file_name)
    # window_to_stop_on = "BioinformaticsWalkthrough_LoadCellParameters"
    # while biwt.window.__class__.__name__ != window_to_stop_on:
    #     print(f"Current window: {str(type(biwt.window))}")
    #     try: 
    #         if biwt.window.__class__.__name__ == "BioinformaticsWalkthroughWindow_PositionsWindow":
    #             biwt.window.biwt_plot_window.plot_cell_pos()
    #         biwt.window.process_window()
    #     except Exception as e:
    #         print(f"Error reaching {window_to_stop_on}: {e}")
    #         break

from collections import defaultdict

from biwt_rule_engine import load_rules_from_csv

def build_rule_map(rules):
    rule_map = defaultdict(list)

    for r in rules:
        key = (r.cell_type, r.signal)
        rule_map[key].append(r)

    return rule_map


def biwt_load_rules():

    csv_file = "/Users/marwanaji/PhysiCell-Studio.git/bin/biwt_protype_rules.csv"
    csv_file = os.path.expanduser(csv_file)

    rules = load_rules_from_csv(csv_file)
    rule_map = build_rule_map(rules)

    print(f"\n[BIWT DEV] Loaded {len(rules)} rules")
    print(f"[BIWT DEV] Rule map size = {len(rule_map)}\n")

    return rules, rule_map

def biwt_dev_mode(biwt):

    try:
        rules, rule_map = biwt_load_rules()

        biwt.biwt_rules = rules
        biwt.biwt_rule_map = rule_map

    except Exception as e:
        print(f"[BIWT ERROR] {e}")


    file_name = "/Users/marwanaji/PhysiCell-Studio.git/visium_adata.h5ad"
    file_name = os.path.expanduser(file_name)

    print(f"\nImporting {file_name}\n")

    biwt.column_line_edit.setText("cluster")
    biwt.import_file(file_name)

    window_to_stop_on = "BioinformaticsWalkthrough_LoadCellParameters"

    while biwt.window.__class__.__name__ != window_to_stop_on:

        try:
            if biwt.window.__class__.__name__ == "BioinformaticsWalkthroughWindow_PositionsWindow":
                biwt.window.biwt_plot_window.plot_cell_pos()

            biwt.window.process_window()

        except Exception as e:
            print(f"Error reaching {window_to_stop_on}: {e}")
            break
