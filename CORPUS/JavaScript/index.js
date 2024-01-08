import fs from 'fs';
import cld from 'cld';
import { XMLParser } from 'fast-xml-parser';
import { ChartJSNodeCanvas } from 'chartjs-node-canvas';

// SETUP
// -----

let inputFile = '';
let noteRepartition = {
    '0,5' : 0,
    '1,0' : 0,
    '1,5' : 0,
    '2,0' : 0,
    '2,5' : 0,
    '3,0' : 0,
    '3,5' : 0,
    '4,0' : 0,
    '4,5' : 0,
    '5,0' : 0
};
let comStorage = {
    charCount: {},
    wordCount: {},
    languageCount : {},
    emojiCount: {},
};
let movieStorage = {};
let movieDistribStorage = {
    'avgNote': {}
};
let userDistribStorage = {
    'avgNote': {}
};
let userStorage = {};
let generalResults = '';
const chartJSNodeCanvas = new ChartJSNodeCanvas({ width: 1000, height: 600, backgroundColour: 'white'});

// GETTING THE INPUT AND OUTPUT FILES
// ----------------------------------

if (process.argv.length >= 3 && process.argv[2] !== '') {
    inputFile = process.argv[2];
} else {
    console.error('Input file expected!');
    process.exit(1);
}

if (process.argv[3] && process.argv[3] != '') {
    outputFile = process.argv[3];
}


// PARSING THE DATA
// ----------------

let data = null;

const xmlParser = new XMLParser();
try {  
    var rawData = fs.readFileSync(inputFile, 'utf8');
    data = xmlParser.parse(rawData);
} catch(e) {
    console.log('Error:', e.stack);
}

// MAIN LOOP
// ---------
await Promise.all(data.comments.comment.map(async (comment) => {

    // COM CHAR COUNT
    if (!comStorage.charCount[comment.commentaire.length]) {
        comStorage.charCount[comment.commentaire.length] = 1;
    } else {
        comStorage.charCount[comment.commentaire.length]++;
    }

    // COM WORD COUNT
    let wordCount = comment.commentaire.trim().split(/\s+/).length;
    if (!comStorage.wordCount[wordCount]) {
        comStorage.wordCount[wordCount] = 1;
    } else {
        comStorage.wordCount[wordCount]++;
    }

    // COM EMOJI COUNT
    let emojiMatches = comment.commentaire.match(/[\p{Emoji}\u200d]+/gu);
    let emojiCount = emojiMatches ? emojiMatches.length : 0;
    if (!comStorage.emojiCount[emojiCount]) {
        comStorage.emojiCount[emojiCount] = 1;
    } else {
        comStorage.emojiCount[emojiCount]++;
    }

    // MOVIE UNIQUE COUNT & AVERAGE NOTE
    if (!movieStorage[comment.movie]) {
        movieStorage[comment.movie] = {
            commentCount : 1,
            totalNote : parseFloat(comment.note)
        }
    } else {
        movieStorage[comment.movie].commentCount++;
        movieStorage[comment.movie].totalNote += parseFloat(comment.note);
    }

    // USER UNIQUE COUNT & AVERAGE NOTE
    if (!userStorage[comment.user_id]) {
        userStorage[comment.user_id] = {
            commentCount : 1,
            totalNote : parseFloat(comment.note)
        }
    } else {
        userStorage[comment.user_id].commentCount++;
        userStorage[comment.user_id].totalNote += parseFloat(comment.note);
    }

    try
    {
        let result = await cld.detect(comment.commentaire, {languageHint : 'FRENCH'});
        
        let language = (result.languages.length > 1 && result.languages[1].name == 'FRENCH') ? 'FRENCH' : result.languages[0].name;

        if(language && language > '' && language != 'FRENCH')
        {
            // COM LANGUAGE
            if (!comStorage.languageCount[language]) 
            {
                comStorage.languageCount[language] = 1;
            } else 
            {
                comStorage.languageCount[language]++;
            }
        }
    }
    catch (error) 
    {}

    // GLOBAL NOTE REPARTITION
    noteRepartition[comment.note]++;
}));

Object.values(movieStorage).forEach(ms => {
    let average = (ms.totalNote / ms.commentCount).toFixed(1);
    if (!movieDistribStorage.avgNote[average]) {
        movieDistribStorage.avgNote[average] = 1;
    } else {
        movieDistribStorage.avgNote[average]++;
    }
});

movieDistribStorage.avgNote = Object.keys(movieDistribStorage.avgNote).sort().reduce(
    (obj, key) => { 
        obj[key] = movieDistribStorage.avgNote[key]; 
        return obj;
    }, 
    {}
);

Object.values(userStorage).forEach(us => {
    let average = (us.totalNote / us.commentCount).toFixed(1);
    if (!userDistribStorage.avgNote[average]) {
        userDistribStorage.avgNote[average] = 1;
    } else {
        userDistribStorage.avgNote[average]++;
    }
});

userDistribStorage.avgNote = Object.keys(userDistribStorage.avgNote).sort().reduce(
    (obj, key) => { 
        obj[key] = userDistribStorage.avgNote[key]; 
        return obj;
    }, 
    {}
);




// GENERAL RESULTS
generalResults += ('Nombre de notes : ' + data.comments.comment.length + '\n')
generalResults += ('Nombre de films uniques : ' + Object.keys(movieStorage).length + '\n')
generalResults += ('Nombre d\'utilisateurs uniques : ' + Object.keys(userStorage).length + '\n')
fs.writeFileSync('output/general_results.txt', generalResults);

// NOTE REPARTITION RESULTS
let noteReparitionConfig = {
    type: 'bar',
    data: { labels: Object.keys(noteRepartition), datasets: [{ label: 'Corpus', data: Object.values(noteRepartition), backgroundColor: '#36A2EB' }] },
};
let noteRepartitionData = (await chartJSNodeCanvas.renderToDataURL(noteReparitionConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/note_repartition.png', noteRepartitionData, 'base64');


// COM CHAR COUNT RESULTS
let comCharCountConfig = {
    type: 'bar',
    data: { labels: Object.keys(comStorage.charCount), datasets: [{ label: 'Corpus', data: Object.values(comStorage.charCount), backgroundColor: '#36A2EB' }] },
};
let comCharCountData = (await chartJSNodeCanvas.renderToDataURL(comCharCountConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/com_char_count.png', comCharCountData, 'base64');


// COM WORD COUNT RESULTS
let comWordCountConfig = {
    type: 'bar',
    data: { labels: Object.keys(comStorage.wordCount), datasets: [{ label: 'Corpus', data: Object.values(comStorage.wordCount), backgroundColor: '#36A2EB' }] },
};
let comWordCountData = (await chartJSNodeCanvas.renderToDataURL(comWordCountConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/com_word_count.png', comWordCountData, 'base64');


// COM EMOJI COUNT RESULTS
let comEmojiCountConfig = {
    type: 'bar',
    data: { labels: Object.keys(comStorage.emojiCount), datasets: [{ label: 'Corpus', data: Object.values(comStorage.emojiCount), backgroundColor: '#36A2EB' }] },
};
let comEmojiCountData = (await chartJSNodeCanvas.renderToDataURL(comEmojiCountConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/com_emoji_count.png', comEmojiCountData, 'base64');


// MOVIE COMMENT COUNT RESULTS
let movieComCountConfig = {
    type: 'bar',
    data: { labels: Object.keys(movieStorage), datasets: [{ label: 'Corpus', data: Object.values(movieStorage).map(m => m.commentCount), backgroundColor: '#36A2EB' }] },
    options: {
        scales: {
            xAxes: {
                display: false
            }
        }
    }
};
let movieComCountData = (await chartJSNodeCanvas.renderToDataURL(movieComCountConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/movie_com_count.png', movieComCountData, 'base64');


// MOVIE AVERAGE NOTE RESULTS
let movieAvgNoteConfig = {
    type: 'bar',
    data: { labels: Object.keys(movieStorage), datasets: [{ label: 'Corpus', data: Object.values(movieStorage).map(m => (m.totalNote / m.commentCount).toFixed(2)), backgroundColor: '#36A2EB' }] },
    options: {
        scales: {
            xAxes: {
                display: false
            }
        }
    }
};
let movieAvgNoteData = (await chartJSNodeCanvas.renderToDataURL(movieAvgNoteConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/movie_avg_note.png', movieAvgNoteData, 'base64');


// USER COMMENT COUNT RESULTS
let userComCountConfig = {
    type: 'bar',
    data: { labels: Object.keys(userStorage), datasets: [{ label: 'Corpus', data: Object.values(userStorage).map(u => u.commentCount), backgroundColor: '#36A2EB' }] },
    options: {
        scales: {
            xAxes: {
                display: false
            }
        }
    }
};
let userComCountData = (await chartJSNodeCanvas.renderToDataURL(userComCountConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/user_com_count.png', userComCountData, 'base64');

// USER AVERAGE NOTE RESULTS
let userAvgNoteConfig = {
    type: 'bar',
    data: { labels: Object.keys(userStorage), datasets: [{ label: 'Corpus', data: Object.values(userStorage).map(u => (u.totalNote / u.commentCount).toFixed(2)), backgroundColor: '#36A2EB' }] },
    options: {
        scales: {
            xAxes: {
                display: false
            }
        }
    }
};
let userAvgNoteData = (await chartJSNodeCanvas.renderToDataURL(userAvgNoteConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/user_avg_note.png', userAvgNoteData, 'base64');

// NOTES CHAR COUNT RESULTS
let comLanguageCountConfig = {
    type: 'bar',
    data: { labels: Object.keys(comStorage.languageCount), datasets: [{ label: 'Corpus', data: Object.values(comStorage.languageCount), backgroundColor: '#36A2EB' }] },
};
let comLanguageCountData = (await chartJSNodeCanvas.renderToDataURL(comLanguageCountConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/com_language_count.png', comLanguageCountData, 'base64');

// 
let movieAvgNoteDistribConfig = {
    type: 'bar',
    data: { labels: Object.keys(movieDistribStorage.avgNote), datasets: [{ label: 'Corpus', data: Object.values(movieDistribStorage.avgNote), backgroundColor: '#36A2EB' }] },
};
let movieAvgNoteDistribData = (await chartJSNodeCanvas.renderToDataURL(movieAvgNoteDistribConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/movie_avg_note_distrib.png', movieAvgNoteDistribData, 'base64');

// 
let userAvgNoteDistribConfig = {
    type: 'bar',
    data: { labels: Object.keys(userDistribStorage.avgNote), datasets: [{ label: 'Corpus', data: Object.values(userDistribStorage.avgNote), backgroundColor: '#36A2EB' }] },
};
let userAvgNoteDistribData = (await chartJSNodeCanvas.renderToDataURL(userAvgNoteDistribConfig)).replace(/^data:image\/png;base64,/, '');
fs.writeFileSync('output/user_avg_note_distrib.png', userAvgNoteDistribData, 'base64');