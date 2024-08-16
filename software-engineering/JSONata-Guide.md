---
title: JSONata 101
subtitle: JSON to JSON transformation in a easy and efficient way
---

Ever wanted to do JSON to JSON transformation but ended up writing code in Python with a bunch of for if filters and maps. Using the right tool for the job saves you a lot of time and helps you keep a consistent interface.

If you are a fan of command line `jq` I was too, until I wanted to write large JSON to JSON transformations.

1.  JQ doesn’t have linters or good editor support.
2.  Hard to know where the errors are and fix them
3.  Not enough libraries in different programming lanugages

## Introducting JSONata

```
{"FirstName”: “Chandler”, “LastName”: “Bing"}
```

Wanna pick the last name?

```
LastName
```

That’s all. Full name?

```
FirstName & " " &LastName
```

Did I just teach you hello world in JSONata? I totally did. But that’s not what we are here for. After all you can \[read documentation on your own\]([https://docs.jsonata.org/overview](https://docs.jsonata.org/overview))

### You Try

Stedi .com has an amazing playground which is my goto for this. https://www.stedi.com/jsonata/playground

## Example 1 - Reconstructing JSON

### Sample Input

```
{
  "submission_id": "item001",
  "form_fields":[
    {
      "field_id": "field001",
      "field_name":"FirstName",
      "field_value": "Chandler"
    },
    {
      "field_id": "field002",
      "field_name": "LastName",
      "field_value":"Bing"
    }
  ]
}
```

### Expected Output

```
{
  "FirstName": "Chandler",
  "LastName": "Bing"
}
```

JSONata Query

```
$merge($map(form_fields, function($v) {
  {$v.field_name: $v.field_value}
}))
```

## Example 2 - Today’s Date

There aren’t any direct date functions in JSONata. But it has `$now` function which returns current timestamp as string. Combing that with substring method will give you the expected result

```
$substring($now(), 0, 10)
```

## Example 3 - Defining Custom Function

Note how multiline expressions are bounded by `(…)`

```
(
 $square := function($n) { $n * $n };
 $square(10);
)
```

## Example 4 - Filtering Objects

Playground link - [https://stedi.link/Q7qZ5qx](https://stedi.link/Q7qZ5qx)

To get all submissions with age < 30, do this

```
submissions[form_fields[field_name='age' and field_value<30]]
```

and not this

```
submissions.form_fields[field_name='age' and field_value<30]
```

In the former case you’re filtering `submissions` in the latter, you’re filtering `form_fields`

### Example 5 - Selecting Keys

Pick all the first name as an array

```
submissions.form_fields[field_name="FirstName"].field_value
```
