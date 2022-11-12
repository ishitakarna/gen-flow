import axios from "axios";

export default class Api {
    constructor() {
        this.client = null;
        this.api_url = "https://37a2-76-191-27-122.ngrok.io";
    }

    init = () => {

        let headers = {
            Accept: "application/json",
        };

        this.client = axios.create({
            baseURL: this.api_url,
            timeout: 31000,
            headers: headers,
        });

        return this.client;
    };

    getIncompleteWorkFlowsForBO = (buId) => {
        return this.init().get(`/workflows/instances/incomplete/${buId}`);
    };

    getWorkflowsForB = (buId) => {
        return this.init().get(`/workflows/metadata/${buId}`);
    }

    createWorkflowInstanceForB = (workflow) => {
        return this.init().post(`/workflows/instances/add/${workflow.wfId}/${workflow.businessId}`);
    }

    deleteWorkflowInstance = (workflow) => {
        return this.init().delete(`/workflows/instances/delete/${workflow.wfInstanceId}/${workflow.businessId}`);
    }
}