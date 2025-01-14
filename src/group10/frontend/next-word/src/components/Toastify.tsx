import toast from 'typescript-toastify';

export enum MessageType {
    Success = "success",
    Error = "error",
    Warning = "warning",
    Info = "info"
}

export const toastifyMessage = (message: string, messageType: MessageType) => {
    new toast({
        position: "top-right",
        toastMsg: message,
        autoCloseTime: 3000,
        canClose: true,
        showProgress: true,
        pauseOnHover: true,
        pauseOnFocusLoss: true,
        type: messageType,
        theme: "dark"
    });
};