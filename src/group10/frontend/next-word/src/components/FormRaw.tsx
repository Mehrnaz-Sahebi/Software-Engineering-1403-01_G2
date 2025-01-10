import React from 'react';

function FormRaw(props: {htmlFor: string, label: string, id: string, type: string}) {
    return (
        <div className="mb-4">
            <label htmlFor={props.htmlFor} className="block text-gray-700 font-medium mb-2">
                {props.label}
            </label>
            <input
                id={props.id}
                type={props.type}
                className="w-full border border-gray-300 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder={`Enter your ${props.htmlFor}`}
                min={props.type === "number" ? "0" : undefined}
            />
        </div>
    );
}

export default FormRaw;