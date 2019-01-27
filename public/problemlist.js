
<h1> This template is for the question list </h1>
<p> It define a .js file contianing of the templates, it is imported by the script src= </p>

<h3> All Problems </h3>
<table class="table table-striped">
    <thead>
        <tr>
            <th>ID</td>
            <th>Description</td>
        </tr>
    <tbody>
        <tr ng-repeat="prob in problems">
            <td>{{prob.id}}</td>
            <td>{{prob.desc}}</td>
        </tr>
    </tobdy>
</table>
