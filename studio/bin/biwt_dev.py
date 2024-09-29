import os
def biwt_dev_mode(biwt):
        file_name = "~/Downloads/visium_adata.h5ad"
        file_name = os.path.expanduser(file_name) 
        print(f"Importing {file_name}")
        # file_name = "./data/Zhuang-ABCA-1-1.064_raw_wClusterAnnots.h5ad"
        #file_name = "./data/abc/metadata/Zhuang-ABCA-1/20231215/views/cell_metadata_with_cluster_annotation.csv"
        if "Zhuang" in file_name:
            biwt.column_line_edit.setText("subclass")
        elif file_name.lower().endswith(".rds"):
            biwt.column_line_edit.setText("celltype")
        else:
            biwt.column_line_edit.setText("cluster")
        biwt.import_file(file_name)
        window_to_stop_on = "BioinformaticsWalkthroughWindow_WritePositions"
        while biwt.window.__class__.__name__ != window_to_stop_on:
            print(f"Current window: {str(type(biwt.window))}")
            try: 
                if biwt.window.__class__.__name__ == "BioinformaticsWalkthroughWindow_PositionsWindow":
                    if hasattr(biwt.window, 'biwt_plot_window'):
                         biwt.window.biwt_plot_window.plot_cell_pos()
                    else:
                        print("biwt_plot_window attribute does not exist in the current window.")
                biwt.window.process_window()
            except Exception as e:
                print(f"Error reaching {window_to_stop_on}: {e}")
                break