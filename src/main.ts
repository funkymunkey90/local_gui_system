import './index.css';
import { DataMan, eRecrodType } from "./core/data_manager";
import {panel_search_basic, panel_basic_results} from "./core/panels/panel_search_bar"


const app_div = document.getElementById("app") as HTMLDivElement;

app_div.appendChild(panel_search_basic)
app_div.appendChild(panel_basic_results)


window.onload = () => {
    console.log ("Loaded.")
    DataMan.addRecord({"name":"item 1", "prop_1":"value 1"})
    DataMan.addRecord({"name":"item 2", "prop_1":"value 1"}, eRecrodType.NOTE)
    console.log (DataMan.itemRecords)
}