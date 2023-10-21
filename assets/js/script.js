/* Danbooru query consts */
const danbooruUrl = 'https://testbooru.donmai.us';

/* Aibooru query consts */
const aibooruUrl = 'https://aibooru.online'; 

/* gelbooru query consts (Uses PHP) */
const gelbooruUrl = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index';

console.log("example of danbooru get response")
fetch(danbooruUrl + '/posts/23.json') 
    .then(response => response.json())
    .then(data => {
    console.log(data);
    })
    .catch(error => {
    console.error('Error:', error);
    });

console.log("example of aibooru get response")
fetch(aibooruUrl + '/posts/47922.json') 
    .then(response => response.json())
    .then(data => {
    console.log(data);
    })
    .catch(error => {
    console.error('Error:', error);
    });

console.log("Example of Gelbooru get response");
fetch(gelbooruUrl + '&id=9136938')
    .then(response => response.text())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });