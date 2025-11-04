const data = [{religion: 'Christian', religion_count: 14},{religion: 'Muslim', religion_count: 2},{religion: 'Hindu', religion_count: 1}]


const result = data.map(function(item){
    return item.religion
})

const count =  data.map(item=>item.religion_count)


console.log(result)


console.log(count)