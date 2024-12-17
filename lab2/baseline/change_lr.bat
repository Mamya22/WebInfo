@echo off
setlocal EnableDelayedExpansion

set lr_list=0.01 0.0001 0.001
set l2_list=0.0001 0.00001 0.001 0.00005 0.0002

for %%a in (%lr_list%) do (
    for %%b in (%l2_list%) do (
        python main_Embedding_based.py --seed 2024 ^
                                       --use_pretrain 0 ^
                                       --pretrain_model_path "trained_model/Douban/Embedding_based.pth" ^
                                       --cf_batch_size 1024 ^
                                       --kg_batch_size 2048 ^
                                       --test_batch_size 2048 ^
                                       --embed_dim 32 ^
                                       --relation_dim 32 ^
                                       --KG_embedding_type "TransE" ^
                                       --kg_l2loss_lambda %%b ^
                                       --cf_l2loss_lambda %%b ^
                                       --lr %%a ^
                                       --n_epoch 1000 ^
                                       --stopping_steps 10
    )
)

endlocal
