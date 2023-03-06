//Basically copied and adapted from AUTOMATIC1111 implementation of the main UI
// mouseover tooltips for various UI elements in the form of "UI element label"="Tooltip text".

prompt_generator_titles = {
    "Temperature": "A higher temperature will produce more diverse results, but with a higher risk of less coherent text",
    "Max Length": "The maximum number of tokens for the output of the model",
    "Top K": "Strategy is to sample from a shortlist of the top K tokens. This approach allows the other high-scoring tokens a chance of being picked.",
    "Repetition Penalty": "The parameter for repetition penalty. 1.0 means no penalty. Default setting is 1.2. Paper explaining it is linked to Github's readme",
    "How Many To Generate":"The number of results to generate. Not guaranteed if models fails to create them",
    "Generate Using Magic Prompt":"Be aware that sometimes the model fails to produce anything or less than the wanted amount, either try again or use a new prompt in that case"
}

onUiUpdate(function(){
	gradioApp().querySelectorAll('span, button, select, p').forEach(function(span){
		tooltip = prompt_generator_titles[span.textContent];

		if(!tooltip){
		    tooltip = prompt_generator_titles[span.value];
		}

		if(!tooltip){
			for (const c of span.classList) {
				if (c in prompt_generator_titles) {
					tooltip = prompt_generator_titles[c];
					break;
				}
			}
		}

		if(tooltip){
			span.title = tooltip;
		}
	})

	gradioApp().querySelectorAll('select').forEach(function(select){
	    if (select.onchange != null) return;

	    select.onchange = function(){
            select.title = prompt_generator_titles[select.value] || "";
	    }
	})
})
