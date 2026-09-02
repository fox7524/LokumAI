# Brain Growth Layered Projection

## Kaynak

- knowledge_dir: `/Users/fox/Documents/PROJECTS/LokumAI/Lokum1.0/Knowledge`
- total_nodes: 103
- total_edges: 83

## Katman özeti

- raw: 64
- hidden_3: 4
- hidden_4: 6
- hidden_5: 4
- hidden_6: 4
- hidden_7: 4
- hidden_8: 4
- hidden_9: 4
- hidden_10: 4
- index: 5

## Katman geçişleri

- raw_to_index: 32
- hidden_3_to_hidden_4: 5
- hidden_3_to_index: 8
- hidden_4_to_hidden_5: 2
- hidden_7_to_hidden_8: 3
- hidden_8_to_hidden_9: 14
- hidden_9_to_hidden_10: 11
- index_to_index: 8

## Domain kümeleri

- domain/apple_silicon_mlx: node_count=2, internal_edges=1, external_edges=12, layers=hidden_3=1, index=1
- domain/cognitive_graph_rag: node_count=3, internal_edges=0, external_edges=0, layers=hidden_4=1, hidden_5=1, hidden_6=1
- domain/cognitive_graph_rag_routing: node_count=2, internal_edges=1, external_edges=12, layers=hidden_3=1, index=1
- domain/cryptographic_integrity_memory_safety: node_count=2, internal_edges=1, external_edges=12, layers=hidden_3=1, index=1
- domain/edge_security_operations: node_count=2, internal_edges=0, external_edges=0, layers=hidden_5=1, hidden_6=1
- domain/edge_systems: node_count=1, internal_edges=0, external_edges=1, layers=hidden_4=1
- domain/embedded_interrupt_dma: node_count=2, internal_edges=1, external_edges=13, layers=hidden_3=1, index=1
- domain/multi_domain: node_count=5, internal_edges=1, external_edges=4, layers=hidden_4=3, hidden_5=1, hidden_6=1
- domain/resilience_operations: node_count=1, internal_edges=0, external_edges=0, layers=hidden_6=1
- domain/security_execution: node_count=1, internal_edges=0, external_edges=1, layers=hidden_5=1
- domain/security_memory: node_count=1, internal_edges=0, external_edges=1, layers=hidden_4=1
- hardware/apple_mlx: node_count=16, internal_edges=0, external_edges=8, layers=raw=16
- hardware/esp32: node_count=16, internal_edges=0, external_edges=8, layers=raw=16
- hidden_10: node_count=4, internal_edges=0, external_edges=11, layers=hidden_10=4
- hidden_8: node_count=4, internal_edges=0, external_edges=17, layers=hidden_8=4
- hidden_9: node_count=4, internal_edges=0, external_edges=25, layers=hidden_9=4
- navigation/domain_entry: node_count=1, internal_edges=0, external_edges=12, layers=index=1
- raw: node_count=16, internal_edges=0, external_edges=8, layers=raw=16
- reasoning/temporal: node_count=4, internal_edges=0, external_edges=3, layers=hidden_7=4
- system/crypto: node_count=16, internal_edges=0, external_edges=8, layers=raw=16

## Katman bazlı cluster yayılımı

- raw: cluster_count=4, dominant_cluster=hardware/apple_mlx, dominant_cluster_share=0.25
- hidden_3: cluster_count=4, dominant_cluster=domain/apple_silicon_mlx, dominant_cluster_share=0.25
- hidden_4: cluster_count=4, dominant_cluster=domain/multi_domain, dominant_cluster_share=0.5
- hidden_5: cluster_count=4, dominant_cluster=domain/cognitive_graph_rag, dominant_cluster_share=0.25
- hidden_6: cluster_count=4, dominant_cluster=domain/cognitive_graph_rag, dominant_cluster_share=0.25
- hidden_7: cluster_count=1, dominant_cluster=reasoning/temporal, dominant_cluster_share=1.0
- hidden_8: cluster_count=1, dominant_cluster=hidden_8, dominant_cluster_share=1.0
- hidden_9: cluster_count=1, dominant_cluster=hidden_9, dominant_cluster_share=1.0
- hidden_10: cluster_count=1, dominant_cluster=hidden_10, dominant_cluster_share=1.0
- index: cluster_count=5, dominant_cluster=domain/apple_silicon_mlx, dominant_cluster_share=0.2

## Yerleşim kalite skorları

- balance: 0.06
- density: 0.03
- cross_cluster_pressure: 0.94
- readability: 0.36

## Temporal dual graph

- entity_nodes: 12
- event_nodes: 12
- temporal_edges: 8

## Workspace broadcast graph

- thoughtseed_nodes: 4
- policy_nodes: 8
- selection_edges: 8
- broadcast_edges: 8

## Execution package graph

- policy_nodes: 4
- package_nodes: 4
- surface_nodes: 5
- binding_edges: 4
- delivery_edges: 8

## Strategic supervision graph

- signal_nodes: 4
- supervision_nodes: 4
- oversight_nodes: 6
- governance_edges: 4
- oversight_edges: 8

## Düğümler

### raw

- [[RAG_Memory_Cell_01_MLX_Unified_Memory_Model]] (domain=hardware/apple_mlx, incoming=0, outgoing=1, layer_column=0, slot_index=0, x=0, y=-5040)
- [[RAG_Memory_Cell_02_MLX_Zero_Copy_DLPack_and_Buffer_Reusage]] (domain=hardware/apple_mlx, incoming=0, outgoing=1, layer_column=0, slot_index=1, x=0, y=-4880)
- [[RAG_Memory_Cell_03_Metal_Shared_vs_Private_StorageMode]] (domain=hardware/apple_mlx, incoming=0, outgoing=1, layer_column=0, slot_index=2, x=0, y=-4720)
- [[RAG_Memory_Cell_13_MLX_Lazy_Evaluation_And_Stream_Dependency_Barriers]] (domain=hardware/apple_mlx, incoming=0, outgoing=0, layer_column=0, slot_index=3, x=0, y=-4560)
- [[RAG_Memory_Cell_14_Metal_Heap_Residency_And_Buffer_Alias_Reuse]] (domain=hardware/apple_mlx, incoming=0, outgoing=0, layer_column=0, slot_index=4, x=0, y=-4400)
- [[RAG_Memory_Cell_15_Apple_Silicon_UMA_Pressure_And_Page_Migration_Signals]] (domain=hardware/apple_mlx, incoming=0, outgoing=0, layer_column=0, slot_index=5, x=0, y=-4240)
- [[RAG_Memory_Cell_16_MLX_Graph_Capture_And_Kernel_Fusion_Boundaries]] (domain=hardware/apple_mlx, incoming=0, outgoing=0, layer_column=0, slot_index=6, x=0, y=-4080)
- [[RAG_Memory_Cell_17_Metal_Argument_Buffers_For_Batched_Dispatch_Coordination]] (domain=hardware/apple_mlx, incoming=0, outgoing=1, layer_column=0, slot_index=7, x=0, y=-3920)
- [[RAG_Memory_Cell_18_MPS_Versus_MLX_Execution_Surface_Selection]] (domain=hardware/apple_mlx, incoming=0, outgoing=1, layer_column=0, slot_index=8, x=0, y=-3760)
- [[RAG_Memory_Cell_19_AMX_Neural_Engine_And_GPU_Scheduling_Tradeoffs]] (domain=hardware/apple_mlx, incoming=0, outgoing=0, layer_column=0, slot_index=9, x=0, y=-3600)
- [[RAG_Memory_Cell_20_Metal_Command_Buffer_Commit_Latency_And_Queue_Depth]] (domain=hardware/apple_mlx, incoming=0, outgoing=0, layer_column=0, slot_index=10, x=0, y=-3440)
- [[RAG_Memory_Cell_21_Unified_Memory_Backpressure_In_Token_Streaming_Pipelines]] (domain=hardware/apple_mlx, incoming=0, outgoing=0, layer_column=0, slot_index=11, x=0, y=-3280)
- [[RAG_Memory_Cell_22_Zero_Copy_Tensor_Interop_Between_MLX_And_Pytorch]] (domain=hardware/apple_mlx, incoming=0, outgoing=0, layer_column=0, slot_index=12, x=0, y=-3120)
- [[RAG_Memory_Cell_23_Sparse_Attention_On_Apple_Silicon_Memory_Budget]] (domain=hardware/apple_mlx, incoming=0, outgoing=1, layer_column=0, slot_index=13, x=0, y=-2960)
- [[RAG_Memory_Cell_24_Quantized_KV_Cache_Placement_On_UMA]] (domain=hardware/apple_mlx, incoming=0, outgoing=1, layer_column=0, slot_index=14, x=0, y=-2800)
- [[RAG_Memory_Cell_25_Metal_Resource_Hazard_Tracking_And_Explicit_Fencing]] (domain=hardware/apple_mlx, incoming=0, outgoing=1, layer_column=0, slot_index=15, x=0, y=-2640)
- [[RAG_Memory_Cell_04_ESP32_FreeRTOS_SMP_Core_Affinity]] (domain=hardware/esp32, incoming=0, outgoing=1, layer_column=0, slot_index=16, x=0, y=-2480)
- [[RAG_Memory_Cell_05_ESP32_Interrupt_Allocation_and_Shared_ISR]] (domain=hardware/esp32, incoming=0, outgoing=1, layer_column=0, slot_index=17, x=0, y=-2320)
- [[RAG_Memory_Cell_06_ESP32_DMA_Capable_Memory_and_ISR_Preallocation]] (domain=hardware/esp32, incoming=0, outgoing=1, layer_column=0, slot_index=18, x=0, y=-2160)
- [[RAG_Memory_Cell_26_ESP32_IRAM_Safe_ISR_Latency_Budgets]] (domain=hardware/esp32, incoming=0, outgoing=0, layer_column=0, slot_index=19, x=0, y=-2000)
- [[RAG_Memory_Cell_27_ESP32_Task_Watchdog_And_Core_Starvation_Patterns]] (domain=hardware/esp32, incoming=0, outgoing=0, layer_column=0, slot_index=20, x=0, y=-1840)
- [[RAG_Memory_Cell_28_Freertos_Queue_Sets_Versus_Direct_Task_Notifications]] (domain=hardware/esp32, incoming=0, outgoing=0, layer_column=0, slot_index=21, x=0, y=-1680)
- [[RAG_Memory_Cell_29_ESP32_Flash_Cache_Disable_Windows_And_Critical_Paths]] (domain=hardware/esp32, incoming=0, outgoing=0, layer_column=0, slot_index=22, x=0, y=-1520)
- [[RAG_Memory_Cell_30_GPIO_Matrix_Interrupt_Fan_In_And_Signal_Jitter]] (domain=hardware/esp32, incoming=0, outgoing=1, layer_column=0, slot_index=23, x=0, y=-1360)
- [[RAG_Memory_Cell_31_RMT_Peripheral_Timing_Determinism_Under_System_Load]] (domain=hardware/esp32, incoming=0, outgoing=1, layer_column=0, slot_index=24, x=0, y=-1200)
- [[RAG_Memory_Cell_32_I2S_DMA_Descriptor_Rings_On_ESP32]] (domain=hardware/esp32, incoming=0, outgoing=0, layer_column=0, slot_index=25, x=0, y=-1040)
- [[RAG_Memory_Cell_33_SPI_DMA_Burst_Alignment_And_Cache_Coherency]] (domain=hardware/esp32, incoming=0, outgoing=0, layer_column=0, slot_index=26, x=0, y=-880)
- [[RAG_Memory_Cell_34_UART_ISR_Backpressure_And_Ring_Buffer_Design]] (domain=hardware/esp32, incoming=0, outgoing=0, layer_column=0, slot_index=27, x=0, y=-720)
- [[RAG_Memory_Cell_35_Freertos_Event_Groups_Versus_Semaphores_For_Driver_States]] (domain=hardware/esp32, incoming=0, outgoing=0, layer_column=0, slot_index=28, x=0, y=-560)
- [[RAG_Memory_Cell_36_PSRAM_Access_Penalties_In_Real_Time_Paths]] (domain=hardware/esp32, incoming=0, outgoing=1, layer_column=0, slot_index=29, x=0, y=-400)
- [[RAG_Memory_Cell_37_Multi_Core_Critical_Sections_And_Spinlock_Contention]] (domain=hardware/esp32, incoming=0, outgoing=1, layer_column=0, slot_index=30, x=0, y=-240)
- [[RAG_Memory_Cell_38_Tickless_Idle_And_Wake_Latency_On_ESP32]] (domain=hardware/esp32, incoming=0, outgoing=1, layer_column=0, slot_index=31, x=0, y=-80)
- [[RAG_Memory_Cell_10_GNN_Message_Passing_for_Graph_Retrieval]] (domain=raw, incoming=0, outgoing=1, layer_column=0, slot_index=32, x=0, y=80)
- [[RAG_Memory_Cell_11_GLM_RAG_Semantic_Graph_Fusion]] (domain=raw, incoming=0, outgoing=1, layer_column=0, slot_index=33, x=0, y=240)
- [[RAG_Memory_Cell_12_Cognitive_RAG_SingleHop_vs_MultiHop_Routing]] (domain=raw, incoming=0, outgoing=1, layer_column=0, slot_index=34, x=0, y=400)
- [[RAG_Memory_Cell_52_Hybrid_Sparse_Dense_Graph_Retrieval]] (domain=raw, incoming=0, outgoing=0, layer_column=0, slot_index=35, x=0, y=560)
- [[RAG_Memory_Cell_53_Graph_Expansion_Budgeting_And_Beam_Search]] (domain=raw, incoming=0, outgoing=0, layer_column=0, slot_index=36, x=0, y=720)
- [[RAG_Memory_Cell_54_Query_Decomposition_For_Multi_Hop_Retrieval]] (domain=raw, incoming=0, outgoing=0, layer_column=0, slot_index=37, x=0, y=880)
- [[RAG_Memory_Cell_55_Edge_Reweighting_From_Retriever_Feedback]] (domain=raw, incoming=0, outgoing=0, layer_column=0, slot_index=38, x=0, y=1040)
- [[RAG_Memory_Cell_56_Temporal_Edges_In_Episodic_Memory_Graphs]] (domain=raw, incoming=0, outgoing=1, layer_column=0, slot_index=39, x=0, y=1200)
- [[RAG_Memory_Cell_57_Entity_Resolution_As_Graph_Construction_Discipline]] (domain=raw, incoming=0, outgoing=1, layer_column=0, slot_index=40, x=0, y=1360)
- [[RAG_Memory_Cell_58_Cross_Encoder_Reranking_After_Graph_Traversal]] (domain=raw, incoming=0, outgoing=0, layer_column=0, slot_index=41, x=0, y=1520)
- [[RAG_Memory_Cell_59_Subgraph_Packing_For_Context_Window_Control]] (domain=raw, incoming=0, outgoing=0, layer_column=0, slot_index=42, x=0, y=1680)
- [[RAG_Memory_Cell_60_Semantic_Drift_Detection_In_Graph_RAG]] (domain=raw, incoming=0, outgoing=0, layer_column=0, slot_index=43, x=0, y=1840)
- [[RAG_Memory_Cell_61_Negative_Sampling_For_Relation_Aware_Embeddings]] (domain=raw, incoming=0, outgoing=0, layer_column=0, slot_index=44, x=0, y=2000)
- [[RAG_Memory_Cell_62_Graph_Neighborhood_Pruning_Under_Token_Budgets]] (domain=raw, incoming=0, outgoing=1, layer_column=0, slot_index=45, x=0, y=2160)
- [[RAG_Memory_Cell_63_Tool_Augmented_Retrieval_Routing_Policies]] (domain=raw, incoming=0, outgoing=1, layer_column=0, slot_index=46, x=0, y=2320)
- [[RAG_Memory_Cell_64_Citation_Grounding_Across_Multi_Source_Reasoning]] (domain=raw, incoming=0, outgoing=1, layer_column=0, slot_index=47, x=0, y=2480)
- [[RAG_Memory_Cell_07_P2P_Encryption_and_ZKP_Constraint_Surface]] (domain=system/crypto, incoming=0, outgoing=1, layer_column=0, slot_index=48, x=0, y=2640)
- [[RAG_Memory_Cell_08_Apple_PAC_Runtime_Integrity]] (domain=system/crypto, incoming=0, outgoing=1, layer_column=0, slot_index=49, x=0, y=2800)
- [[RAG_Memory_Cell_09_Memory_Safety_Primitives_and_Failure_Signatures]] (domain=system/crypto, incoming=0, outgoing=1, layer_column=0, slot_index=50, x=0, y=2960)
- [[RAG_Memory_Cell_39_Pointer_Authentication_Key_Domains_And_Signing_Contexts]] (domain=system/crypto, incoming=0, outgoing=0, layer_column=0, slot_index=51, x=0, y=3120)
- [[RAG_Memory_Cell_40_Control_Flow_Integrity_And_PAC_Complementarity]] (domain=system/crypto, incoming=0, outgoing=0, layer_column=0, slot_index=52, x=0, y=3280)
- [[RAG_Memory_Cell_41_Use_After_Free_Telemetry_And_Crash_Clustering]] (domain=system/crypto, incoming=0, outgoing=0, layer_column=0, slot_index=53, x=0, y=3440)
- [[RAG_Memory_Cell_42_Heap_Metadata_Corruption_Signatures]] (domain=system/crypto, incoming=0, outgoing=0, layer_column=0, slot_index=54, x=0, y=3600)
- [[RAG_Memory_Cell_43_Stack_Canary_Failure_Telemetry_And_Triage]] (domain=system/crypto, incoming=0, outgoing=1, layer_column=0, slot_index=55, x=0, y=3760)
- [[RAG_Memory_Cell_44_Secure_Enclave_Boundaries_And_Key_Ladder_Separation]] (domain=system/crypto, incoming=0, outgoing=1, layer_column=0, slot_index=56, x=0, y=3920)
- [[RAG_Memory_Cell_45_AEAD_Nonce_Reuse_Failure_Modes]] (domain=system/crypto, incoming=0, outgoing=0, layer_column=0, slot_index=57, x=0, y=4080)
- [[RAG_Memory_Cell_46_Zero_Knowledge_Proof_Witness_Exposure_Surfaces]] (domain=system/crypto, incoming=0, outgoing=0, layer_column=0, slot_index=58, x=0, y=4240)
- [[RAG_Memory_Cell_47_Merkle_Commitments_For_Retrieval_Integrity]] (domain=system/crypto, incoming=0, outgoing=0, layer_column=0, slot_index=59, x=0, y=4400)
- [[RAG_Memory_Cell_48_Forward_Secrecy_In_Peer_To_Peer_Session_Rotation]] (domain=system/crypto, incoming=0, outgoing=0, layer_column=0, slot_index=60, x=0, y=4560)
- [[RAG_Memory_Cell_49_Remote_Attestation_Signals_For_Edge_Nodes]] (domain=system/crypto, incoming=0, outgoing=1, layer_column=0, slot_index=61, x=0, y=4720)
- [[RAG_Memory_Cell_50_Memory_Disclosure_Versus_Code_Reuse_Attack_Paths]] (domain=system/crypto, incoming=0, outgoing=1, layer_column=0, slot_index=62, x=0, y=4880)
- [[RAG_Memory_Cell_51_Crash_Triage_For_Memory_Safety_Regressions]] (domain=system/crypto, incoming=0, outgoing=1, layer_column=0, slot_index=63, x=0, y=5040)

### hidden_3

- [[H3_Apple_Silicon_Memory_Execution_Synthesis]] (domain=domain/apple_silicon_mlx, incoming=0, outgoing=3, layer_column=1, slot_index=0, x=240, y=-240)
- [[H3_Cognitive_Graph_RAG_Routing_Synthesis]] (domain=domain/cognitive_graph_rag_routing, incoming=0, outgoing=3, layer_column=1, slot_index=1, x=240, y=-80)
- [[H3_Cryptographic_Integrity_And_Memory_Safety_Synthesis]] (domain=domain/cryptographic_integrity_memory_safety, incoming=0, outgoing=3, layer_column=1, slot_index=2, x=240, y=80)
- [[H3_Embedded_Interrupt_DMA_Synthesis]] (domain=domain/embedded_interrupt_dma, incoming=0, outgoing=4, layer_column=1, slot_index=3, x=240, y=240)

### hidden_4

- [[H4_Cognitive_Retrieval_Policy_Selection]] (domain=domain/cognitive_graph_rag, incoming=0, outgoing=0, layer_column=2, slot_index=0, x=480, y=-400)
- [[H4_Edge_Device_Response_Strategy]] (domain=domain/edge_systems, incoming=1, outgoing=0, layer_column=2, slot_index=1, x=480, y=-240)
- [[H4_Cross_Domain_Causal_Alignment]] (domain=domain/multi_domain, incoming=0, outgoing=1, layer_column=2, slot_index=2, x=480, y=-80)
- [[H4_Performance_Bottleneck_Disambiguation]] (domain=domain/multi_domain, incoming=1, outgoing=0, layer_column=2, slot_index=3, x=480, y=80)
- [[H4_Resource_Execution_Prioritization]] (domain=domain/multi_domain, incoming=2, outgoing=1, layer_column=2, slot_index=4, x=480, y=240)
- [[H4_Security_Failure_Mode_Arbitration]] (domain=domain/security_memory, incoming=1, outgoing=0, layer_column=2, slot_index=5, x=480, y=400)

### hidden_5

- [[H5_Retrieval_Depth_Governance]] (domain=domain/cognitive_graph_rag, incoming=0, outgoing=0, layer_column=3, slot_index=0, x=720, y=-240)
- [[H5_Global_Escalation_Gate]] (domain=domain/edge_security_operations, incoming=0, outgoing=0, layer_column=3, slot_index=1, x=720, y=-80)
- [[H5_Metacognitive_Policy_Arbitration]] (domain=domain/multi_domain, incoming=1, outgoing=0, layer_column=3, slot_index=2, x=720, y=80)
- [[H5_Risk_Performance_Tradeoff_Control]] (domain=domain/security_execution, incoming=1, outgoing=0, layer_column=3, slot_index=3, x=720, y=240)

### hidden_6

- [[H6_Retrieval_Action_Coordination]] (domain=domain/cognitive_graph_rag, incoming=0, outgoing=0, layer_column=4, slot_index=0, x=960, y=-240)
- [[H6_Global_Response_Orchestration]] (domain=domain/edge_security_operations, incoming=0, outgoing=0, layer_column=4, slot_index=1, x=960, y=-80)
- [[H6_Executive_Priority_Orchestration]] (domain=domain/multi_domain, incoming=0, outgoing=0, layer_column=4, slot_index=2, x=960, y=80)
- [[H6_Recovery_Execution_Sequencing]] (domain=domain/resilience_operations, incoming=0, outgoing=0, layer_column=4, slot_index=3, x=960, y=240)

### hidden_7

- [[H7_Episodic_Timeline_Alignment]] (domain=reasoning/temporal, incoming=0, outgoing=1, layer_column=5, slot_index=0, x=1200, y=-240)
- [[H7_Event_Entity_Binding]] (domain=reasoning/temporal, incoming=0, outgoing=1, layer_column=5, slot_index=1, x=1200, y=-80)
- [[H7_Recency_Drift_Governance]] (domain=reasoning/temporal, incoming=0, outgoing=0, layer_column=5, slot_index=2, x=1200, y=80)
- [[H7_Temporal_Causal_Recall]] (domain=reasoning/temporal, incoming=0, outgoing=1, layer_column=5, slot_index=3, x=1200, y=240)

### hidden_8

- [[H8_Decision_Commitment_Gate]] (domain=hidden_8, incoming=1, outgoing=3, layer_column=6, slot_index=0, x=1440, y=-240)
- [[H8_Dominant_Thoughtseed_Selection]] (domain=hidden_8, incoming=2, outgoing=4, layer_column=6, slot_index=1, x=1440, y=-80)
- [[H8_Exception_Override_Arbitration]] (domain=hidden_8, incoming=0, outgoing=4, layer_column=6, slot_index=2, x=1440, y=80)
- [[H8_Global_Policy_Broadcast]] (domain=hidden_8, incoming=0, outgoing=3, layer_column=6, slot_index=3, x=1440, y=240)

### hidden_9

- [[H9_Commit_Ready_Delivery_Check]] (domain=hidden_9, incoming=4, outgoing=2, layer_column=7, slot_index=0, x=1680, y=-240)
- [[H9_Execution_Surface_Binding]] (domain=hidden_9, incoming=4, outgoing=4, layer_column=7, slot_index=1, x=1680, y=-80)
- [[H9_Failsafe_Action_Packaging]] (domain=hidden_9, incoming=2, outgoing=3, layer_column=7, slot_index=2, x=1680, y=80)
- [[H9_Response_Payload_Composition]] (domain=hidden_9, incoming=4, outgoing=2, layer_column=7, slot_index=3, x=1680, y=240)

### hidden_10

- [[H10_Global_Supervision_Arbitration]] (domain=hidden_10, incoming=3, outgoing=0, layer_column=8, slot_index=0, x=1920, y=-240)
- [[H10_Long_Horizon_Outcome_Review]] (domain=hidden_10, incoming=3, outgoing=0, layer_column=8, slot_index=1, x=1920, y=-80)
- [[H10_Rollback_Escalation_Governance]] (domain=hidden_10, incoming=2, outgoing=0, layer_column=8, slot_index=2, x=1920, y=80)
- [[H10_Strategic_Resource_Oversight]] (domain=hidden_10, incoming=3, outgoing=0, layer_column=8, slot_index=3, x=1920, y=240)

### index

- [[Index_Apple_Silicon_and_MLX]] (domain=domain/apple_silicon_mlx, incoming=10, outgoing=1, layer_column=9, slot_index=0, x=2160, y=-320)
- [[Index_Cognitive_Graph_RAG]] (domain=domain/cognitive_graph_rag_routing, incoming=10, outgoing=1, layer_column=9, slot_index=1, x=2160, y=-160)
- [[Index_Cryptography_and_Memory_Safety]] (domain=domain/cryptographic_integrity_memory_safety, incoming=10, outgoing=1, layer_column=9, slot_index=2, x=2160, y=0)
- [[Index_Embedded_and_ESP32]] (domain=domain/embedded_interrupt_dma, incoming=10, outgoing=1, layer_column=9, slot_index=3, x=2160, y=160)
- [[Brain_Growth_Index]] (domain=navigation/domain_entry, incoming=8, outgoing=4, layer_column=9, slot_index=4, x=2160, y=320)
