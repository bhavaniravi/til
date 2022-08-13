# How to set a fixed height for all Grid rows?

When I was building 100Ideas there was a small requirement that when the ideas grow large it shouldn't affect the layout of the grid, the row and column height of the grid element should be fixed

### Before

![](<../../.gitbook/assets/image (2).png>)

### After

![](<../../.gitbook/assets/image (1).png>)

### Code&#x20;

#### HTML



```
  <div className='container'>
      <div className='content'>
           <div className='item'/>
           <div className='item'/>
      </div>
  </div>
```

#### CSS

Setting `grid-auto-rows` does the trick

```
.content {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-auto-rows: 10rem; // this does the trick
  grid-gap: 2% 2%
}
```
