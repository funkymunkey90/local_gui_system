
// ----------------------------------------------
// Record Item
// ----------------------------------------------

class Panel_Search_Basic extends HTMLDivElement {
    private static _instance: Panel_Search_Basic | null = null;
    
    public input_search:HTMLInputElement = document.createElement('input') as HTMLInputElement
    public button_search:HTMLButtonElement = document.createElement('button') as HTMLButtonElement

    constructor () {
        super()
        // const ShadowRoot = this.attachShadow({mode:'open'})
        this.classList.add('panel-search-basic')

        this.input_search.type = "text";
        this.input_search.id = 'saerch-input';
        this.input_search.placeholder = "Search...";
        this.input_search.classList.add('search-input')

        this.button_search.type = "submit";
        this.button_search.id = "button-submit"
        this.button_search.disabled = false;
        this.button_search.textContent = 'Search'
        this.button_search.classList.add('button-submit')

        this.appendChild(this.input_search)
        this.appendChild(this.button_search)
    }

    public static getInstance () : Panel_Search_Basic {
        if (!Panel_Search_Basic._instance) {
            Panel_Search_Basic._instance = document.createElement("div", { is: "panel-search-basic" }) as Panel_Search_Basic;
        }
        return Panel_Search_Basic._instance;
    }

    connectedCallback () {
        console.log('panel_search_basic added to DOM')
    }
}

class Panel_Basic_Results extends HTMLDivElement {
    private static _instance: Panel_Basic_Results | null = null;

    constructor () {
        super()
        // const ShadowRoot = this.attachShadow({mode:'open'})
        this.classList.add('panel-results-basic')
    }
    
    public static getInstance () : Panel_Basic_Results {
        if (!Panel_Basic_Results._instance) {
            Panel_Basic_Results._instance = document.createElement("div", { is: "panel-results-basic" }) as Panel_Basic_Results;
        }
        return Panel_Basic_Results._instance;
    }
    
}

customElements.define ('panel-search-basic', Panel_Search_Basic, { extends: "div" })
customElements.define ('panel-results-basic', Panel_Basic_Results, { extends: "div" })
export const panel_search_basic = Panel_Search_Basic.getInstance()
export const panel_basic_results = Panel_Basic_Results.getInstance()