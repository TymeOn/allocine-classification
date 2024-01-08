import * as cheerio from 'cheerio';
import { create } from 'xmlbuilder2';
import * as fs from 'fs';

let globalRequests = [];
let requests = [];
let results = create().ele('comments');
let status = {
  '2,5' : {
    count : 0,
    limit : 66281
  },
  '2,0' : {
    count : 0,
    limit : 69715
  },
  '1,5' : {
    count : 0,
    limit : 98051
  },
  '1,0' : {
    count : 0,
    limit : 94774
  },
  '0,5' : {
    count : 0,
    limit : 86628
  }
}


// Iterate over all movies
for (let m = 287126; m >= 267126; m--) {
  if (!movieList.includes(m.toString())) {
    console.log('// Processing movie : ' + m);

    await new Promise(r => setTimeout(r, 1));

    let pageCount = 0;
    globalRequests.push(
      fetch('https://www.allocine.fr/film/fichefilm-' + m + '/critiques/spectateurs/')
      .then(response => response.text())  
      .then(async(body) => {
        const page = cheerio.load(body);
        pageCount = page('.pagination-item-holder').children('.item').last().text();

        // Iterate over all comment pages
        for (let i = 1; i <= pageCount; i++) {
          
          console.log('-- Fetching page ' + i + '/' + pageCount);

          await new Promise(r => setTimeout(r, 1));

          requests.push(
            fetch('https://www.allocine.fr/film/fichefilm-<MOVIE_ID>/critiques/spectateurs/?page='.replace('<MOVIE_ID>', m) + i)
            .then(response => response.text())  
            .then((body) => {
              const page = cheerio.load(body);
              page('.review-card').each((i, el) => {
                const note = page(el).find('.stareval-note').text();
                if (status[note] && status[note].count < status[note].limit) {
                  results.ele('comment')
                  .ele('commentaire').txt(page(el).find('.review-card-content').text()).up()
                  .ele('note').txt(note).up()
                  .up();
                  status[note].count++;
                }
              });
            })
          );
        }
      })
    )
  }
};

try {
  await Promise.all(globalRequests);
  await Promise.all(requests);
  console.log('// Writing results');
  const xml = results.end({ prettyPrint: true });
  fs.writeFileSync('results.xml', xml);
} catch (err) {
  console.error(err)
}
