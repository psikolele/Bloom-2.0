import json
import uuid

# Load the workflow
input_path = r"c:\Users\psiko\Desktop\Antigravity\Bloom 2.0\backup_workflows\Caption_Flow_V3_ANALYSIS.json"
output_path = r"c:\Users\psiko\Desktop\Antigravity\Bloom 2.0\backup_workflows\Caption_Flow_V3_VIDEO_MOD.json"

try:
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        workflow = json.load(f)

    nodes = workflow['nodes']
    connections = workflow['connections']

    # --- 1. FIND NODES ---
    # Find existing nodes to connect to/from
    prepare_input_node = next(n for n in nodes if "Prepare Input Variables" in n['name'])
    generate_concept_node = next(n for n in nodes if "Generate Content Concept" in n['name'])
    
    # Find the video nodes (currently disconnected)
    video_prompt_node = next(n for n in nodes if n['name'] == "Video Prompt3")
    text_to_video_node = next(n for n in nodes if n['name'] == "Text to Video2")
    
    # --- 2. CREATE IF NODE (Check Format) ---
    if_node_id = str(uuid.uuid4())
    if_node = {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict",
                    "version": 2
                },
                "conditions": [
                    {
                        "id": str(uuid.uuid4()),
                        "leftValue": "={{ $json.format }}",
                        "rightValue": "video",
                        "operator": {
                            "type": "string",
                            "operation": "equals",
                            "name": "filter.operator.equals"
                        }
                    }
                ],
                "combinator": "and"
            }
        },
        "id": if_node_id,
        "name": "Check Format",
        "type": "n8n-nodes-base.if",
        "typeVersion": 2.2,
        "position": [
            prepare_input_node['position'][0] + 200, 
            prepare_input_node['position'][1]
        ]
    }
    nodes.append(if_node)

    # --- 3. FIX VIDEO PROMPT (Dynamic Prompt) ---
    # Change from hardcoded string to dynamic expression using the concept
    # "value": "={{ $('3a. Generate Content Concept (Gemini)').item.json.output.ideas[0].concept }}"
    for assignment in video_prompt_node['parameters']['assignments']['assignments']:
        if assignment['name'] == 'video_prompt':
            assignment['value'] = "={{ $('3a. Generate Content Concept (Gemini)').item.json.output.ideas[0].concept }}"
            print(f"Updated Video Prompt to dynamic value: {assignment['value']}")

    # --- 4. UPDATE CONNECTIONS ---
    
    # Remove connection from Prepare Input -> Generate Concept (we insert IF node here)
    if "2. Prepare Input Variables (Topic, Audience, etc.)" in connections:
        del connections["2. Prepare Input Variables (Topic, Audience, etc.)"]

    # Connect Prepare Input -> Check Format
    connections["2. Prepare Input Variables (Topic, Audience, etc.)"] = {
        "main": [
            [
                {
                    "node": "Check Format",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }

    # Connect Check Format (False/Image) -> Generate Concept (Existing path)
    if "Check Format" not in connections:
        connections["Check Format"] = {"main": [[], []]} # [True(Video), False(Image)]
    
    connections["Check Format"]["main"][1].append({
        "node": "3a. Generate Content Concept (Gemini)",
        "type": "main",
        "index": 0
    })

    # Connect Check Format (True/Video) -> Generate Concept (We reuse the concept generation for now)
    # Actually, we need to generate concept FIRST, then Branch?
    # No, the user wants to choose format. 
    # The Concept Generation is shared? 
    # Let's see: Concept Generation produces "ideas". 
    # If we branch BEFORE concept, needed separate concept node?
    # Re-reading plan: "If Check Format is video: Generate Content Concept (Reuse existing 3a)"
    # PROPOSAL: Move IF node *AFTER* "Generate Content Concept"?
    # If we move after, we generate concept for both. Then branching decides if we make Image Prompt or Video Prompt.
    # This seems cleaner and safer.
    
    # REVISED STRATEGY: 
    # 1. Restore original connection: Prepare Input -> Generate Concept
    # 2. Insert IF node AFTER "Generate Content Concept"
    # 3. IF node checks format.
    #    - False (Image): Goes to "3b. Generate Image Prompt Options"
    #    - True (Video): Goes to "Video Prompt3"
    
    print("Switching strategy: Placing IF node after Concept Generation")
    
    # Remove connection from Concept -> Image Prompt
    if "3a. Generate Content Concept (Gemini)" in connections:
        del connections["3a. Generate Content Concept (Gemini)"]
        
    # Connect Prepare Input -> Generate Concept (Ensure it exists)
    connections["2. Prepare Input Variables (Topic, Audience, etc.)"] = {
        "main": [[{"node": "3a. Generate Content Concept (Gemini)", "type": "main", "index": 0}]]
    }

    # Connect Generate Concept -> Check Format
    connections["3a. Generate Content Concept (Gemini)"] = {
        "main": [[{"node": "Check Format", "type": "main", "index": 0}]]
    }
    
    # Position Check Format
    if_node['position'] = [
        generate_concept_node['position'][0] + 250,
        generate_concept_node['position'][1]
    ]

    # Connect Check Format (False/Image) -> 3b. Generate Image Prompt Options
    connections["Check Format"]["main"][1] = [{
        "node": "3b. Generate Image Prompt Options (Gemini)",
        "type": "main",
        "index": 0
    }]

    # Connect Check Format (True/Video) -> Video Prompt3
    connections["Check Format"]["main"][0] = [{
        "node": "Video Prompt3",
        "type": "main",
        "index": 0
    }]

    # Ensure Video Prompt3 connects to Text to Video2
    connections["Video Prompt3"] = {
        "main": [[{"node": "Text to Video2", "type": "main", "index": 0}]]
    }
    
    # Text to Video2 -> Wait4 -> Get Video4 -> If4 -> Video URL4 is likely already connected or needs check.
    # From previous dump, they seemed sequential but lets make sure.
    connections["Text to Video2"] = {"main": [[{"node": "Wait4", "type": "main", "index": 0}]]}
    connections["Wait4"] = {"main": [[{"node": "Get Video4", "type": "main", "index": 0}]]}
    connections["Get Video4"] = {"main": [[{"node": "If4", "type": "main", "index": 0}]]}
    connections["If4"] = {"main": [[
        {"node": "Video URL4", "type": "main", "index": 0} # True/Success path
    ], [
        {"node": "Wait4", "type": "main", "index": 0} # False/Not ready -> Loop back to Wait?
        # WARNING: Looping needs care. Usually Wait node has a loop.
        # Let's check If4 logic. If state != success, we might need a loop or fail.
        # For simple flows, we might just stop. But usually we want to loop back to Get Video.
        # Let's assume standard pattern: If4(False) -> Wait4.
    ]]}
    
    # Connect Loop for If4 (False)
    connections["If4"]["main"][1] = [{"node": "Wait4", "type": "main", "index": 0}]

    # --- 5. CONNECT VIDEO OUTPUT TO REST OF FLOW ---
    # Video URL4 needs to go effectively to "Respond to Frontend" and "Check via Email".
    # The existing flow merges at "5. Prepare Data for Instagram API" (Image).
    # We should probably merge both paths into "5. Prepare Data..." or a new Set node?
    # "5. Prepare Data..." sets "ImageURL" and "Caption".
    # We can create a "Prepare Video Data" set node or update "5. Prepare Data" to handle video too.
    # Let's connect Video URL4 -> "5. Prepare Data for Instagram API"
    # And we update "5. Prepare Data" parameters to handle video url if present.

    connections["Video URL4"] = {
        "main": [[{"node": "5. Prepare Data for Instagram API", "type": "main", "index": 0}]]
    }

    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=4)

    print(f"Successfully created modified workflow: {output_path}")

except Exception as e:
    print(f"Error modifying workflow: {e}")
