//  Script para exibir um arquivo pdf no template html
const container = document.getElementById('pdf-container');
const examId = container.dataset.examId; // obtém exam.id do atributo dos dados
pdfjsLib.getDocument("{% url 'ManageLab:proxy_pdf' exam.id %}").promise.then(pdf => {
    pdf.getPage(1).then(page => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        const viewport = page.getViewport({  scale: 0.6 });

        canvas.width = viewport.width;
        canvas.height = viewport.height;

        page.render({ canvasContext: context, viewport }).promise.then(() => {
            container.appendChild(canvas);
        });
    })
})
