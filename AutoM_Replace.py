import unreal

def replace_instance():
    #获取当前所有选中物体
    select_asset = unreal.EditorLevelLibrary.get_selected_level_actors()
    asset_tool = unreal.AssetToolsHelpers.get_asset_tools()

    count = 0
    unreal.log("请选择场景中的材质会自动替换材质为实例")
    if not select_asset:
        unreal.log_warning("你没有在 3D 视口中选中物体！请直接去场景里选。")
        return

    count = 0
    for asset in select_asset:

        unreal.log("检查中")
        comps = asset.get_components_by_class(unreal.StaticMeshComponent)
        if not comps:
            continue

        for comp in comps:
            num_materials = comp.get_num_materials()
            comp_Cg = False

        for i in range(num_materials):
            m_in = comp.get_material(i)
            if not m_in:
                continue
            if isinstance(m_in,unreal.Material):
                master_mat = m_in
                old_name = master_mat.get_name()
                mat_path = master_mat.get_path_name()

                if mat_path.startswith("/Engine/"):
                    unreal.log(f"{old_name}这是默认材质跳过")
                    continue
                b_name = old_name
                if b_name.startswith("M_"):
                    b_name = b_name[2:]
                                #实例规范命名
                mi_name = f"MI_{b_name}"
                p_path = unreal.Paths.get_path(mat_path)
                mi_full_path = f"{p_path}/{mi_name}.{mi_name}"
                mi_asset = None

                                #是否存在同名
                if unreal.EditorAssetLibrary.does_asset_exist(mi_full_path):
                    mi_asset = unreal.EditorAssetLibrary.load_asset(mi_full_path)
                    unreal.log(f"{mi_name}这个实例已经有了就用这个")
                else:
                    #创建新实例
                    unreal.log(f"创建新实例{mi_name}")
                    mi_f = unreal.MaterialInstanceConstantFactoryNew()
                    mi_asset = asset_tool.create_asset(mi_name, p_path, unreal.MaterialInstanceConstant, mi_f)
                    unreal.MaterialEditingLibrary.set_material_instance_parent(mi_asset, master_mat)
                    unreal.EditorAssetLibrary.save_asset(mi_asset.get_path_name())
                comp.set_material(i, mi_asset)
                comp_Cg = True
            if comp_Cg:
                count += 1

        unreal.log(f"处理完了，{count} 个模型不是材质实例")
replace_instance()
