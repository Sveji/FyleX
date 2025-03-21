
import PropTypes from "prop-types";
import { Worker, Viewer, SpecialZoomLevel } from "@react-pdf-viewer/core";

import "@react-pdf-viewer/highlight/lib/styles/index.css";
import * as pdfjsLib from "pdfjs-dist";

import "@react-pdf-viewer/default-layout/lib/styles/index.css";
import { useEffect, useState } from "react";
import { searchPlugin } from "@react-pdf-viewer/search";

const workerUrl = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.js`;

PDFView.propTypes = {
    pdfUrl: PropTypes.string.isRequired,
    highlightedText: PropTypes.string.isRequired,
};

export default function PDFView({ pdfUrl, keywords = [] }) {
    // const searchPluginInstance = searchPlugin();
    console.log(keywords)


    const searchPluginInstance = searchPlugin({
        keyword: [...keywords]
    })
    const { highlight } = searchPluginInstance;

    const [documentLoad, onDocumentLoad] = useState(false);
    const [highlightedText, setHighlightedText] = useState('')

    const handleDocumentLoad = () => {
        onDocumentLoad(true);
    };

    useEffect(() => {
        if (documentLoad === true && highlightedText !== "") {
            console.log(highlightedText);
            // highlightPlugin.highlight(highlightedText);
            highlight(highlightedText);
            console.log("highlighted");
        }
    }, [documentLoad, highlightedText]);

    // const styles = StyleSheet.create({
    //     page: { backgroundColor: 'tomato' },
    //     section: { color: 'white', textAlign: 'center', margin: 30 }
    // });

    return (
        <div className="border-solid border-2 rounded-md border-slate-300 h-screen w-auto overflow-auto overscroll-contain">
            <Worker workerUrl={workerUrl} style={styles.page}>
                <Viewer
                    style={styles.section}
                    fileUrl={pdfUrl}
                    onDocumentLoad={handleDocumentLoad}
                    plugins={[searchPluginInstance]}
                />
            </Worker>
        </div>
    );
}