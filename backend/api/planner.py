# In ai_planner.py

def inject_voiceover_logic(template_code: str, ai_script: str, ai_data: str) -> str:
    """
    This is the "Logic Injector." 
    It takes your static template and merges it with Gemini's generated explanation.
    """
    # 1. Add the necessary imports to the top of the script
    voice_imports = (
        "from manim_voiceover import VoiceoverScene\n"
        "from manim_voiceover.services.gtts import GTTSService\n"
    )
    
    # 2. Update the class definition to use VoiceoverScene
    refined_code = template_code.replace("class DynamicScene(Scene):", "class DynamicScene(VoiceoverScene):")
    
    # 3. Inject the speech service setup
    setup_logic = "        self.set_speech_service(GTTSService())\n"
    refined_code = refined_code.replace("def construct(self):", f"def construct(self):\n{setup_logic}")
    
    # 4. Replace placeholders with AI content
    # We assume your templates have markers like #DATA_HERE and #SCRIPT_HERE
    refined_code = refined_code.replace("#DATA_HERE", ai_data)
    refined_code = refined_code.replace("#SCRIPT_HERE", f"speech_text = \"{ai_script}\"")
    
    return voice_imports + refined_code