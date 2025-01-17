import React from 'react';

function LinkLabel(props: {text: string, link: string, linkText: string}) {
    return (
        <p className="text-center text-gray-600 m-6">
            {props.text + " "}
            <br/>
            <a href={props.link} className="text-blue-500 hover:underline">
                {props.linkText}
            </a>
        </p>
    );
}

export default LinkLabel;