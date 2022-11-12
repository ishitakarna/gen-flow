import axios from "axios";

export default class Api {
    constructor() {
        this.client = null;
        this.api_url = "https://83aa-76-191-27-122.ngrok.io";
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

    loginUser = (email, password) => {
        let body = {
            email: email,
            passwd: password
        }
        return this.init().post(`/user/login`, body);
    }

    searchWorkflowInstanceId = (wfId) =>{
        return this.init().get(`/workflows/instances/search/${wfId}`);
    }
    deleteWorkflowInstance = (workflow) => {
        return this.init().delete(`/workflows/instances/delete/${workflow.wfInstanceId}/${workflow.businessId}`);
    }

    getWorkflowsForP = (userId) => {
        return this.init().get(`/workflows/instances/po/${userId}`);
    }

    getWorkflowDetails = (wfInstId) => {
        return this.init().get(`/workflows/instances/search/${wfInstId}`);
    }

    getReport = (buId) => {
        return this.init().get(`/workflows/instances/report/${buId}`);
    }

    completedProcess = (pInstId, wfInstId, pId) => {
        let body = {
            processInstanceId: pInstId,
            wfInstanceId: wfInstId,
            processId: pId
        }
        return this.init().post(`/process/complete`, body);
    }
}